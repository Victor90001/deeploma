$(document).ready(function(){
    $("#width_value").text("Ширина: "+$("#width_input").val());
    $("#width_input").on("input", function(){
        $("#width_value").text("Ширина: "+$(this).val());
    });

    $("#height_value").text("Высота: "+$("#height_input").val());
    $("#height_input").on("input", function(){
        $("#height_value").text("Высота: "+$(this).val());
    });

    $("#conf_value").text($("#conf").val());
    $("#conf").on("input", function(){
        $("#conf_value").text($(this).val());
    });

    $("#iou_value").text($("#iou").val());
    $("#iou").on("input", function(){
        $("#iou_value").text($(this).val());
    });

    $("#uploadFile").on("change", function(){
        if(this.files[0].size > 5120){
            alert("Размер файла не должен превышать 5 Мб");
            $(this).val("")
        }
    });
})
