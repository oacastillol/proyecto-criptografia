$(document).ready(function(){
    $('#cifrar').click(
	function(){
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
		    console.log(data );
		    $('#messageOut').val(data.message);
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if ( console && console.log ) {
			console.log( "La solicitud a fallado: " +  textStatus);
		    }
		});
	});
    $('#descifrar').click(
	function(){
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
		    console.log(data );
		    $('#messageOut').val(data.message);
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if ( console && console.log ) {
			console.log( "La solicitud a fallado: " +  textStatus);
		    }
		});
	});
    $('#entrar').click(function(){
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
		$('#myLogin').modal('hide');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		localStorage.setItem("token-user",data.jwt_token);
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if ( console && console.log ) {
		    console.log( "La solicitud a fallado: " +  textStatus);
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
	    contentType: "application/json; charset=utf-8",
	    url: "/api/v1/users/",
	})
	    .done(function( data ) {
		$('#myLogin').modal('hide');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
		console.log(data);
		localStorage.setItem("token-user",data.jwt_token);
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if ( console && console.log ) {
		    console.log( "La solicitud a fallado: " +  textStatus);
		}
	    });
    });
    $('#messages').click(function(){
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
			    console.log(e);
			    $('#tbodyM').append(`<tr>
 <td>
				<div class="radio" id="valor`+e.id+`">
				    <label>
					<input type="radio" name="valor`+e.id+`" >`+e.title+`</label>
							   </div>
			    </td>
			    <td>`+e.cipher+`</td>
							   </tr>`);
			});
		    $("#myMessage").modal();
		})
		.fail(function( jqXHR, textStatus, errorThrown ) {
		    if ( console && console.log ) {
			console.log( "La solicitud a fallado: " +  textStatus);
		    }
		});
	}
    });
    $('#guardar').click(function(){
	if (localStorage.getItem("token-user")  !== null){
	    let cipher = $('#messageOut').val();
	    let title = $('#titleMessage').val();
	    let dataFill = JSON.stringify({"title":title,
					   "cipher":cipher
					  });
	    let headersFill= {"api-token":localStorage.getItem("token-user")};
	    $.ajax({
		data:dataFill,
		type: 'POST',
		dataType: "json",
		headers: headersFill,
		contentType: "application/json; charset=utf-8",
		url: "/api/v1/messages/",
	    })
	    .done(function( data ) {
		console.log(data );
	    })
	    .fail(function( jqXHR, textStatus, errorThrown ) {
		if ( console && console.log ) {
		    console.log( "La solicitud a fallado: " +  textStatus);
		}
	    });
	}});
    $('#logout').click(function(){
	console.log("salir");
	localStorage.removeItem("token-user");
    });
});
