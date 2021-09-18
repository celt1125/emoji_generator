function Generate(){
    let raw_text = document.getElementById("raw_text").value;
    let input_text = raw_text.split('\n');
	let min_emoji_num_text = document.getElementById("min_emoji_num").value;
	let max_emoji_num_text = document.getElementById("max_emoji_num").value;
	
	if (min_emoji_num_text == "" || max_emoji_num_text == ""){
		document.getElementById("result").value = "請輸入表情數量";
		return;
	}
	if (isNaN(min_emoji_num_text) || isNaN(max_emoji_num_text)){
		document.getElementById("result").value = "請在表情數量輸入數字";
		return;
	}
	let min_emoji_num = parseInt(min_emoji_num_text);
	let max_emoji_num = parseInt(max_emoji_num_text);
	if (min_emoji_num > max_emoji_num){
		document.getElementById("result").value = "請輸入符合邏輯的表情數量";
		return;
	}
	if (min_emoji_num < 0){
		document.getElementById("result").value = "請輸入符合邏輯的表情數量";
		return;
	}
    
    let output_text = "";
    input_text.forEach(sentence => {
		if (sentence == ""){
			output_text += "\n";
			return;
		}
		
		var word_list = [];
		for (let i = 0; i < sentence.length; i++)
			word_list.push(sentence.substring(i, i+1));
		for (let i = 0; i < sentence.length - 1; i++)
			word_list.push(sentence.substring(i, i+2));
		for (let i = 0; i < sentence.length - 2; i++)
			word_list.push(sentence.substring(i, i+3));
		
		var emoji_list = [];
		word_list.forEach(word => {
			if (word in database){
				database[word].forEach(emoji => {
					emoji_list.push(emoji);
				});
			}
		});
		
		
		let emoji_num = randintRange(min_emoji_num, max_emoji_num);
		if (emoji_list.length == 0){
			let index = randint(database["random"].length);
			let postfix = database["random"][index].repeat(emoji_num);
			output_text += `${sentence}${postfix} \n`;
		}
		else{
			let index = randint(emoji_list.length);
			let postfix = emoji_list[index].repeat(emoji_num);
			output_text += `${sentence}${postfix} \n`;
		}
    });

    document.getElementById("result").value = output_text;
}

function randint(n){
    return Math.floor(Math.random() * n);
}

function randintRange(a, b){
	return a + Math.floor(Math.random() * (b - a + 1));
}