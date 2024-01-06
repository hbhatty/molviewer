$(document).ready(function () {
    $.get("/info", function (data, status) {
        // if(status == 200){
        $("#molID").empty();
        let test = []
        if (data.length > 0) {
            test = data.split(" ")
            let lengtharr = test.length;
            for (let i = 0; i < lengtharr; i++) {
                $("#molID").append("<option>" + test[i] + "</option>");
            }
        } else {
            $("#molID").append("<option>" + "Empty" + "</option>");
        }

    })
    $.get("/getno", function (data, status) {
        $("#molID2").empty();
        let test3 = []
        if (data.length > 0) {
            test3 = data.split(",");
            let lengtharr = test3.length;
            if (lengtharr == 2) {
                $("#molID2").append("<option>" + test3[0] + "</option>");
            } else {
                for (let i = 0; i < lengtharr - 1; i++) {
                    $("#molID2").append("<option>" + test3[i] + "</option>");
                }
            }
        } else {
            $("#molID2").append("<option>" + "Empty" + "</option>");
        }
    })

    // Get value on button click and show alert
    $("#add").click(function (event) {
        event.preventDefault();
        var elnum = $("#elenumber").val()
        var elcode = $("#elecode").val();
        var check = false;
        var elname = $("#elename").val();
        var check2 = false;
        var elecol1 = $("#elecol1").val()
        var elecol2 = $("#elecol2").val()
        var elecol3 = $("#elecol3").val()
        var rad = $("#rad").val()
        elnum = parseInt(elnum)
        rad = parseFloat(rad)
        $.get("/checkcode", function (data, status) {
            let test = []
            if (data.length > 0) {
                test = data.split(" ")
                if (jQuery.inArray($("#elecode").val(), test) != -1) {
                    check2 = true;
                } else {
                    check2 = false;
                }
            }
            if (check2 == false) {
                if ($("#elenumber").val().length == 0 || $("#elecode").val().length == 0 || $("#elename").val().length == 0 || $("#elecol1").val().length == 0 || $("#elecol2").val().length == 0 || $("#elecol3").val().length == 0) {
                    alert("Missing fields");
                    check = false;
                }
                else if (elnum <= 0 || elnum > 118) {
                    check = false;
                    alert("Something wrong with element number");
                    $("#elenumber").css("border", "1px solid #cc1703");
                } else if (elecol1.length != 6 || elecol2.length != 6 || elecol3.length != 6) {
                    check = false;
                    alert("Colour value error")
                    $("#elecol1").val("");
                    $("#elecol2").val("");
                    $("#elecol3").val("");
                } else if (isNaN(rad)) {
                    check = false;
                    alert("Incorrect input for radius!")
                    $("#rad").css("border", "1px solid #cc1703");
                }
                else if (elname.length > 13) {
                    check = false;
                    alert("Element Name is too large!")
                    $("#elename").css("border", "1px solid #cc1703");
                }
                else if (rad <= 0 || rad >= 999) {
                    alert("Radius is less than 0/Radius is too large!")
                    $("#rad").css("border", "1px solid #cc1703");
                    check = false;
                }
                else {
                    check = true
                }

                var formData = {
                    elnum: parseInt($("#elenumber").val()),
                    elcode: $("#elecode").val(),
                    elname: $("#elename").val(),
                    elecol1: $("#elecol1").val(),
                    elecol2: $("#elecol2").val(),
                    elecol3: $("#elecol3").val(),
                    rad: parseFloat($("#rad").val()),
                };
                if (check == true) {
                    alert("Element has been added!");
                    $("#elenumber").css("border", "1px solid #ccc");
                    $("#elecode").css("border", "1px solid #ccc");
                    $("#elecol1").css("border", "1px solid #ccc");
                    $("#elecol2").css("border", "1px solid #ccc");
                    $("#elecol3").css("border", "1px solid #ccc");
                    $("#elename").css("border", "1px solid #ccc");
                    $("#rad").css("border", "1px solid #ccc");
                    $("#elenumber").val("");
                    $("#elename").val("");
                    $("#elecode").val("");
                    $("#elecol1").val("");
                    $("#elecol2").val("");
                    $("#elecol3").val("");
                    $("#rad").val("");
                    $.ajax({
                        url: "/addelement",
                        type: "POST",
                        dataType: "json",
                        data: JSON.stringify(formData),
                        success: function (res) {
                            console.log(res);
                        }
                    })
                    $.get("/info", function (data, status) {
                        // if(status == 200){
                        $("#molID").empty();
                        let test = []
                        test = data.split(" ")
                        let lengtharr = test.length;
                        for (let i = 0; i < lengtharr; i++) {
                            $("#molID").append("<option>" + test[i] + "</option>");
                        }
                    })
                }
            } else {
                alert("Element Code Already Exists!")
            }
        })

    });
    $("#delete").click(function (event) {
        let temp = $("#molID").val();
        if (temp == "Empty" || temp.length == 0) {
            alert("List is empty! Add something in order to delete")
        } else {
            alert("Deleted!")
            $.ajax({
                url: "/deleteelement",
                type: "POST",
                data: temp,
                dataType: "text",
                success: function () {
                    $.get("/info", function (data, status) {
                        $("#molID").empty();
                        let test = []
                        if (data.length > 0) {
                            test = data.split(" ")
                            let lengtharr = test.length;
                            for (let i = 0; i < lengtharr; i++) {
                                $("#molID").append("<option>" + test[i] + "</option>");
                            }
                        } else {
                            $("#molID").append("<option>" + "Empty" + "</option>");
                        }
                    })
                }
            })
        }
    })

    $("#uploadMol").click(function (event) {
        event.preventDefault();
        var validExtensions = ["sdf"]
        // var temp = document.getElementById("sdf_file").value
        var file = $("#sdf_file").val().split('.').pop();
        var filename = $('input[type=file]').val().replace(/.*(\/|\\)/, '');
        var check3 = false;
        var sendObj = {
            name: $("#uploadfile").val(),
            fname: filename
        }
        if ($("#uploadfile").val().length == 0) {
            alert("Empty name!")
        }
        else if (validExtensions.indexOf(file) == -1) {
            alert("Only sdf files are allowed!")
        } else {
            $.get("/checkmol", function (data, status) {
                let test = []
                test = data.split(" ")
                if (jQuery.inArray($("#uploadfile").val(), test) != -1) {
                    check3 = true;
                } else {
                    check3 = false;
                }
                if (check3 == false) {
                    alert("Success File Added!");
                    $.ajax({
                        url: "/addmol",
                        type: "POST",
                        // dataType: "json",
                        data: JSON.stringify(sendObj),
                        success: function () {
                            $.get("/getno", function (data, status) {
                                $("#molID2").empty();
                                let test3 = []
                                test3 = data.split(",");
                                let lengtharr = test3.length;
                                if (lengtharr == 2) {
                                    $("#molID2").append("<option>" + test3[0] + "</option>");
                                } else {
                                    for (let i = 0; i < lengtharr - 1; i++) {
                                        $("#molID2").append("<option>" + test3[i] + "</option>");
                                    }
                                }
                            })
                        }
                    })
                } else {
                    alert("Invalid Name/Already Used!");
                }
            })
        }
    })
    $("#display").click(function () {
        var selected = $("#molID2").val()
        var checkDisplay = true;
        if (selected == "Empty" || selected == null) {
            checkDisplay = false
        }
        hold = selected.split(" ");
        var sendData = {
            select: hold[1]
        }
        if (checkDisplay == true) {

            $.ajax({
                url: "/displaymol",
                type: "POST",
                data: JSON.stringify(sendData),
                success: function (res) {
                    // alert(res)
                    // $("#displayMolecule").append(res)
                    let svg = res
                    let blob = new Blob([svg], { type: "image/svg+xml" })
                    let url = URL.createObjectURL(blob)
                    let image = document.getElementById("displayMol")
                    image.src = url;
                    image.addEventListener("load", () => URL.revokeObjectURL(url), { once: true })
                    document.getElementById("edittext").innerHTML = "Here is your molecule: " + sendData.select
                    $('#divhide2').css('display', 'block');
                    $('#divhide').css('display', 'block');
                }
            })
        }
        else {
            alert("There are no molecules, add one!");
        }
    })
    $("#rotatex").click(function () {
        var selected = $("#molID2").val()
        hold = selected.split(" ");
        var sendData = {
            select: hold[1],
            xInput: $("#rotatechoice").val(),
        }
        var sendData2 = {
            select: hold[1]
        }
        var check = parseInt($("#rotatechoice").val())
        if (isNaN(check) || check > 360 || check < -360) {
            alert("Not a valid angle!");
        } else if (check == 0) {
            $.ajax({
                url: "/displaymol",
                type: "POST",
                data: JSON.stringify(sendData2),
                success: function (res) {
                    // $("#displayMolecule").append(res)
                    let svg = res
                    let blob = new Blob([svg], { type: "image/svg+xml" })
                    let url = URL.createObjectURL(blob)
                    let image = document.getElementById("displayMol")
                    image.src = url;
                    image.addEventListener("load", () => URL.revokeObjectURL(url), { once: true })
                }
            })
        }
        else {
            $.ajax({
                url: "/rotatemolx",
                type: "POST",
                data: JSON.stringify(sendData),
                success: function (res) {
                    let svg2 = res
                    let blob2 = new Blob([svg2], { type: "image/svg+xml" })
                    let url2 = URL.createObjectURL(blob2)
                    let image2 = document.getElementById("displayMol")
                    image2.src = url2;
                    image2.addEventListener("load", () => URL.revokeObjectURL(url2), { once: true })
                }

            })
        }
    })
    $("#rotatey").click(function () {
        var selected = $("#molID2").val()
        hold = selected.split(" ");
        var sendData = {
            select: hold[1],
            yInput: $("#rotatechoice").val(),
        }
        var sendData2 = {
            select: hold[1]
        }
        var check = parseInt($("#rotatechoice").val())
        if (isNaN(check) || check > 360 || check < -360) {
            alert("Not a valid angle!");
        } else if (check == 0) {
            $.ajax({
                url: "/displaymol",
                type: "POST",
                data: JSON.stringify(sendData2),
                success: function (res) {
                    // $("#displayMolecule").append(res)
                    let svg = res
                    let blob = new Blob([svg], { type: "image/svg+xml" })
                    let url = URL.createObjectURL(blob)
                    let image = document.getElementById("displayMol")
                    image.src = url;
                    image.addEventListener("load", () => URL.revokeObjectURL(url), { once: true })
                }
            })
        }
        else {
            $.ajax({
                url: "/rotatemoly",
                type: "POST",
                data: JSON.stringify(sendData),
                success: function (res) {
                    let svg2 = res
                    let blob2 = new Blob([svg2], { type: "image/svg+xml" })
                    let url2 = URL.createObjectURL(blob2)
                    let image2 = document.getElementById("displayMol")
                    image2.src = url2;
                    image2.addEventListener("load", () => URL.revokeObjectURL(url2), { once: true })
                }

            })
        }
    })
    $("#rotatez").click(function () {
        var selected = $("#molID2").val()
        hold = selected.split(" ");
        var sendData = {
            select: hold[1],
            zInput: $("#rotatechoice").val(),
        }
        var sendData2 = {
            select: hold[1]
        }
        var check = parseInt($("#rotatechoice").val())
        if (isNaN(check) || check > 360 || check < -360) {
            alert("Not a valid angle!");
        }
         else if (check == 0) {
            $.ajax({
                url: "/displaymol",
                type: "POST",
                data: JSON.stringify(sendData2),
                success: function (res) {
                    // $("#displayMolecule").append(res)
                    let svg = res
                    let blob = new Blob([svg], { type: "image/svg+xml" })
                    let url = URL.createObjectURL(blob)
                    let image = document.getElementById("displayMol")
                    image.src = url;
                    image.addEventListener("load", () => URL.revokeObjectURL(url), { once: true })
                }
            })
        }
        
        else {
            $.ajax({
                url: "/rotatemolz",
                type: "POST",
                data: JSON.stringify(sendData),
                success: function (res) {
                    let svg2 = res
                    let blob2 = new Blob([svg2], { type: "image/svg+xml" })
                    let url2 = URL.createObjectURL(blob2)
                    let image2 = document.getElementById("displayMol")
                    image2.src = url2;
                    image2.addEventListener("load", () => URL.revokeObjectURL(url2), { once: true })
                }

            })
        }
    })

});

function validateInput(input) {
    var regex = /[^a-z]/gi;
    input.value = input.value.replace(regex, "")
}

function valInput(input) {
    var regex = /[^a-fA-F0-9]/gi;
    input.value = input.value.replace(regex, "");
}

function valInput2(text) {
    var regex = /[^0-9]\d*$/gi;
    text.value = text.value.replace(regex, "");
}