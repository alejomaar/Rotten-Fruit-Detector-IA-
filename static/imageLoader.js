function $(id){
    return document.getElementById(id);
}

$("form").addEventListener('submit', (e)=>{
    
    e.preventDefault();
    var formdata = new FormData($("form"))
    fetch('/edges',{
        method: 'POST',
        body: formdata
    }).then(res =>res.json())
    .then(data =>{
        console.log(data);
        RenderResults(data);
        drawChart(data);
    })
});

function RenderResults(data){
    var FruitSet ={
        "oranges" : "Naranja",
        "apple": "Manzana",
        "banana": "Banana"
    }
    var RottenSet ={
        "bad" : "podrida",
        "good": "buena"
    }
    predictFruit = FruitSet[data.fruit]
    predictRotten = RottenSet[data.state]
    message = predictFruit+" "+predictRotten;

    $("classificationMessage").innerHTML = message;
}

$("file").onchange = function (evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;
    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            $("imagePreview").src = fr.result;
            $("imagePreview").style.height = "100%";
        }
        fr.readAsDataURL(files[0]);
        PreviewImage()
        $("auxiliar").click();
    }
    else {
        console.log("Not supported")

    }
}
//Remover etiquetas cuando la imagen carge
function PreviewImage(){
    $("form").style.display= "none";
}