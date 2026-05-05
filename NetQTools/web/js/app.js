/* global hljs */


function sendRequest(){
    var amb = $("#amb").val();
    var tipoid = $("#tipoid").val();
    
    //alert("amb: "+amb+"  |  tipoid: "+tipoid);
    sendID(amb,tipoid);
}



function sendID(env,tipoid){
    if(env === 'sapa'){
        var x = document.getElementById("sapaID").value;
    }else{
        var x = document.getElementById("submitID").value;
    }
    
    $("#resposta").html("");
    swal({
    title: 'Wait!',
    text: 'processing...',
    timer: 1,
    showConfirmButton: false,
    imageUrl: 'images/30.gif',
    onOpen: () => {
        swal.showLoading()
    }
    }).then((result) => {
        if (result.dismiss === swal.DismissReason.timer){
            $.ajax({
                type: 'POST',
                data: {id: x, req: env, tid: tipoid,chld: 0},
                url: 'URLRequest',
                async:false,
                timeout:5000,
                success: function(data){
                    $("#resposta").html(data);
                    document.getElementById("submitID").value="";
                    document.getElementById("sapaID").value="";
                    if(env === 'sapa' || tipoid != 'netq'){
                        hljs.initHighlighting.called = false;
                        hljs.initHighlighting();
                    }
                }
            });
        }
    })
}

function validateAC(){
    var ac = document.getElementById("submitAC").value;
    var acRGEX = /^[0-9]{2}[A-Z]{2}[0-9]{2}$/;
    var acResult = acRGEX.test(ac);
    if(acResult == false){
        alert('A area central terá que ter o formato "00XX00"');
    }else{
        sendRequestSigra(ac);
    }
}

function sendRequestSigra(ac){
    //var ac = document.getElementById("submitAC").value;  
    //alert("amb: "+amb+"  |  tipoid: "+tipoid);
    
    $("#resposta").html("");
    swal({
    title: 'Wait!',
    text: 'processing...',
    timer: 1,
    showConfirmButton: false,
    imageUrl: 'images/30.gif',
    onOpen: () => {
        swal.showLoading()
    }
    }).then((result) => {
        if (result.dismiss === swal.DismissReason.timer){
            $.ajax({
                type: 'POST',
                data: {ac: ac},
                url: 'URLRequestSigra',
                async:false,
                timeout:5000,
                success: function(data){
                    $("#resposta").html(data);
                    document.getElementById("submitAC").value="";
                    
                    hljs.initHighlighting.called = false;
                    hljs.initHighlighting();
                    
                }
            });
        }
    })
}



function fillRegisto(idRequest,div){
    var divSide="left";
    if(div!=="div"){
        divSide="right";
    }
    
    if ($("#"+div+idRequest).html().length <= 1){
        swal({
            title: 'Wait!',
            text: 'processing...',
            timer: 1,
            showConfirmButton: false,
            imageUrl: 'images/30.gif',
            onOpen: () => {
                swal.showLoading()
            }
        }).then((result) => {
            if (result.dismiss === swal.DismissReason.timer){
                var env = document.getElementById("req").value;
                $.ajax({
                    type: 'POST',
                    data: {id: idRequest, req: env,tid: 'NETQ', chld: 1,div: divSide},
                    url: 'URLRequest',
                    async:false,
                    timeout:5000,
                    success: function(data){
                        $("#"+div+idRequest).html(data); 
                        hljs.initHighlighting.called = false;
                        hljs.initHighlighting();
                    }
                });

            }
        })
    }
}

  

                