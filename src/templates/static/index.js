var pageInitialized = false;
$(document).ready(function(){
    if(pageInitialized) return;
    pageInitialized=true;
    init();
    addFunctions();
});
function init(){
    if (localStorage.getItem("token-user")  !== null){
	userLoged();
    }else{
	userAnon();
	clear();
    }
};
function userLoged(){
    $('#errorAlert').hide();
    $('#liLogin').hide();
    $('#liPerfil').show();
    $('#liMensajes').show();
    $('#liLogout').show();
    $('#divSave').show();
};
function userAnon(){
    $('#liLogin').show() ;
    $('#liPerfil').hide();
    $('#liMensajes').hide();
    $('#liLogout').hide();
    $('#divSave').hide();
};
function clear(){
    clearErrors();
    $('#messageIn').val('');
    $('#key').val('');
    $('#messageOut').val('');
    $('#titleMessage').val('');
    $('#username').val('');
    $('#password').val('');
    $('#usernamePerfil').val('');
    $('#passwordPerfil').val('');
    $("#tbMessages tbody").remove();
    $('#tbMessages').append(`<tbody id="tbodyM"> </tbody>`);
};
function showError(message,modal=undefined){
    if(modal==undefined){
	$('#messageError').html('<strong>Error!</strong> '+message);	
	$('#errorAlert').show();
    }else{
	$('#messageError'+modal).html('<strong>Error!</strong> '+message);	
	$('#errorAlert'+modal).show();
    }
};
function clearErrors(){
    $('#errorAlert').hide();
    $('#messageError').html('');
    $('#errorAlertmyLogin').hide();
    $('#messageErrormyLogin').html('');
    $('#errorAlertmyMessage').hide();
    $('#messageErrormyMessage').html('');
    $('#errorAlertmyPerfil').hide();
    $('#messageErrormyPerfil').html('');
};
function loadMessages(){
    if (localStorage.getItem("token-user")  !== null){
	let headersFill= {"api-token":localStorage.getItem("token-user")};
	$.ajax({
	    type: 'GET',
	    dataType: "json",
	    headers:headersFill,
	    contentType: "application/json; charset=utf-8",
	    url: "/api/v1/messages",
	})
	    .done(function( data ) {
		$("#tbMessages tbody").remove();
		$('#tbMessages').append(`<tbody id="tbodyM"> </tbody>`);
		data.forEach(
		    function(e){
			$('#tbodyM').append(`<tr>
 <td>
				<div class="radio" id="valor`+e.id+`">
				    <label>
					<input type="radio" name="msjId" value="`+e.id+`">  `+e.title+`</label>
							   </div>
			    </td>
			    <td>`+e.cipher+`</td>
							   </tr>`);
		    });
		$("#myMessage").modal();
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error);
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" ... "+errorThrown);
		}
	    });
    }
};
function translate(codes){
    codes.forEach(function(e){
	console.log(String.fromCharCode(e));
    });    
    return String.fromCharCode(codes);
};
function clearMessage(){
    $('#messageOut').html('');
}
function addFunctions(){
    $('#cifrar').click(
	function(){
	    clearMessage();
	    let textIn = $('#messageIn').val();
	    let type = $('#typeCipher').val();
	    let key = $('#key').val();
	    $.ajax({
		data:JSON.stringify({"message":textIn,
				     "type":type,
				     "key":key
				    }), 
		type: 'POST',
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		url: "/api/v1/cipher/encode",
	    })
		.done(function( data ) {
		    $('#messageOut').append(`<p>`+data.message+`</p>`);
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if(typeof jqXHR.responseJSON !== 'undefined' ){
			showError(jqXHR.responseJSON.error);
		    }else{
			showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown);
		    }
		});
	});
    $('#descifrar').click(
	function(){
	    clearMessage();
	    let textIn = $('#messageIn').val();
	    let type = $('#typeCipher').val();
	    let key = $('#key').val();
	    $.ajax({
		data:JSON.stringify({"message":textIn,
				     "type":type,
				     "key":key
				    }), 
		type: 'POST',
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		url: "/api/v1/cipher/decode",
	    })
		.done(function( data ) {
		    $('#messageOut').append(`<p>`+data.message+`</p>`);
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if(typeof jqXHR.responseJSON !== 'undefined' ){
			showError(jqXHR.responseJSON.error);
		    }else{
			showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown);
		    }
		});
	});
    $('#entrar').click(function(){
	clearErrors();
	let user=$('#username').val();
	let pass=$('#password').val();
	let dataFill = JSON.stringify({"username":user,
				       "password":pass
				      });
	$.ajax({
	    data: dataFill,
	    type: 'POST',
	    dataType: "json",
	    contentType: "application/json; charset=utf-8",
	    url: "/api/v1/users/login",
	})
	    .done(function( data ) {
		$('#myLogin').modal('toggle');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		localStorage.setItem("token-user",data.jwt_token);
		init();
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error,"myLogin");
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown,"myLogin");
		}
		
	    });
    });
    $('#registrar').click(function(){
	let user=$('#username').val();
	let pass=$('#password').val();
	let dataFill=JSON.stringify({"username":user,
				     "password":pass
				    });
	$.ajax({
	    data:dataFill, 
	    type: 'POST',
	    dataType: "json",
	    contentType: "application/json",
	    url: "/api/v1/users/",
	})
	    .done(function( data ) {
		$('#myLogin').modal('hide');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		localStorage.setItem("token-user",data.jwt_token);
		init();
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error,"myLogin");
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown,"myLogin");
		}
	    });
    });
    $('#messages').click(function(){
	loadMessages();
    });
    $('#guardar').click(function(event){
	event.preventDefault();
	if (localStorage.getItem("token-user")  !== null){
	    let cipher = $('#messageOut').text();
	    let title = $('#titleMessage').val();
	    let dataFill = JSON.stringify({"title":title,
					   "cipher":cipher
					  });
	    let headersFill= {"api-token":localStorage.getItem("token-user")};
	    if (typeof is_sending !== 'undefined' && is_sending) return false;
	    $.ajax({
		beforeSend: function () {
		    is_sending = true;
		},
		data:dataFill,
		type: 'POST',
		dataType: "json",
		headers: headersFill,
		contentType: "application/json; charset=utf-8",
		url: "/api/v1/messages/",
	    })
		.done(function( data ) {
		    is_sending=false;
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if(typeof jqXHR.responseJSON !== 'undefined' ){
			showError(jqXHR.responseJSON.error);
		    }else{
			showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown);
		    }
		});
	}
	return true;
    });
    $('#perfilBtn').click(function(){
	if (localStorage.getItem("token-user")  !== null){
	    let headersFill= {"api-token":localStorage.getItem("token-user")};
	    $.ajax({
		type: 'GET',
		dataType: "json",
		headers:headersFill,
		contentType: "application/json; charset=utf-8",
		url: "/api/v1/users/me",
	    })
		.done(function( data ) {
		    $("#usernamePerfil").val(data.username);
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if(typeof jqXHR.responseJSON !== 'undefined' ){
			showError(jqXHR.responseJSON.error,"myPerfil");
		    }else{
			showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" ... "+errorThrown,"myPerfil");
		    }
		});
	}
    });
    $("#savePerfil").click(function(){
	let user=$('#usernamePerfil').val();
	let pass=$('#passwordPerfil').val();
	let dataFill = JSON.stringify({"username":user,
				       "password":pass
				      });
	let headersFill= {"api-token":localStorage.getItem("token-user")};
	$.ajax({
	    data: dataFill,
	    headers:headersFill,
	    type: 'PUT',
	    dataType: "json",
	    contentType: "application/json; charset=utf-8",
	    url: "/api/v1/users/me",
	})
	    .done(function( data ) {
		$('#myPerfil').modal('toggle');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		init();
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error,"myPerfil");
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown,"myPerfil");
		}		
	    });
    });
    $("#borrarMsj").click(function(){
	let msj = $('input[name=msjId]:checked').val();
	let urlM = "/api/v1/messages/"+msj;
	let headersFill= {"api-token":localStorage.getItem("token-user")};
	$.ajax({
	    headers:headersFill,
	    type: 'DELETE',
	    dataType: "json",
	    url: urlM,
	})
	    .done(function( data ) {
		loadMessages();
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error,"myPerfil");
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown,"myMessage");
		}		
	    });
    });
    $("#cargarMsj").click(function(){
	let msj = $('input[name=msjId]:checked').val();
	let urlM = "/api/v1/messages/"+msj;
	let headersFill= {"api-token":localStorage.getItem("token-user")};
	$.ajax({
	    headers:headersFill,
	    type: 'GET',
	    dataType: "json",
	    url: urlM,
	})
	    .done(function( data ) {
		$('#myMessage').modal('hide');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		clearMessage();
		$('#messageOut').append(`<p>`+data.cipher+`</p>`);
		$('#titleMessage').val(data.title);
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if(typeof jqXHR.responseJSON !== 'undefined' ){
		    showError(jqXHR.responseJSON.error,"myMessage");
		}else{
		    showError("Lo sentimos no sabemos que ocurrio..."+textStatus+" "+errorThrown,"myMessage");
		}		
	    });
    });
    $('#logout').click(function(){
	localStorage.removeItem("token-user");
	init();
    });
};
