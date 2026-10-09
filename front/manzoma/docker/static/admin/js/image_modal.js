
function imagePopup(imageUrl){
    // let imageUrl="https://10.0.227.16/images/%D8%A7%D9%84%D9%82%D9%88%D8%A7%D8%AA%20%D8%A7%D9%84%D8%A8%D8%AD%D8%B1%D9%8A%D9%87/2000134902479/2026-02-08_18-10-18/2000134902479_6_1.jpg"
    const modal = document.createElement("div");
    modal.className = "modal-overlay";
    modal.innerHTML=`<div class="modal-content">
                        <img id="image-modal-content" src='${imageUrl}' />
                    </div>`;
    document.body.appendChild(modal);
    modal.addEventListener("click",function(){
        modal.style.display = "none";
    });
};

function clearImagePopup(){
    document.querySelector(".modal-overlay").style.display="none";
}

document.addEventListener("DOMContentLoaded",function(){
    const modal = document.createElement("div");
    modal.id = "image-modal";
    modal.innerHTML = `
    <span id="image-modal-close">&times;<span>
    <img id="image-modal-content">
    `;
    document.body.appendChild(modal);
    const modalImg = document.getElementById("image-modal-content");

    document.querySelectorAll(".admin-image--thumbnail").forEach(img => {
        img.addEventListener("click",function(){
            modal.style.display = "flex";
            modalImg.src = this.dataset.fullImage;
        });
    });

    modal.addEventListener("click",function(){
        modal.style.display = "none";
    });

});