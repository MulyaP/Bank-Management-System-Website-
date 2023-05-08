console.log("hiii");

let show = document.getElementById("show-details");

show.addEventListener("click",()=>{
    window.location.href="/users/show-details";
})

let tran = document.getElementById("transfer");

tran.addEventListener("click",()=>{
    window.location.href="/users/transfer";
})