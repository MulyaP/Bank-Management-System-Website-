let btn = document.getElementsByClassName("btn");

for(let i=0;i<btn.length;i++){
    btn[i].addEventListener("click",()=>{
        let inp = btn[i].previousElementSibling;
        inp.removeAttribute("disabled");
    })
}

let sub = document.getElementById("sub");

sub.addEventListener("click",(e)=>{
    let elem = document.getElementsByClassName("inp");

    for (let i=0;i<elem.length;i++){
        elem[i].removeAttribute('disabled');
    }
    let resp = alert("Changes done! Please login again!");
})