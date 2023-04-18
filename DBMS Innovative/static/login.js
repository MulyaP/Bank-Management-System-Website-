const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

let elem = document.getElementsByClassName('btn');
console.log(elem);

// for (let i=0;i<elem.length;i++){
//     elem[i].addEventListener("click",(e)=>{
        
//     })
// }