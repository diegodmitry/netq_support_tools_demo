<%-- 
    Document   : sigra
    Created on : Jan 24, 2019, 4:16:20 PM
    Author     : Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Netq Support tools</title> 
    </head>
    <body>
        <div class="top-bar">
                <div class="top-bar-left">
                    <ul class="menu text_menu">  
                        <li>
                            AREA CENTRAL
                            <input class="app_input" type="text" id="submitAC" placeholder="area central" maxlength="6"/>
                        </li>
                        <li>
                            <button type="submit" class="hollow button secondary " onclick="validateAC()">submit</button>
                        </li>
                    </ul>
                </div>  
            </div>
            <div id="wait" class="wait" style="display: none; z-index: 999; position: absolute; left: 0; right: 0; top: 0; bottom: 0; margin: auto; width: 500px; height: 300px;">
                <img class="wait" src="images/wait.gif" height="75" width="75">
            </div>
            <div id="resposta" class="resposta" >

            </div> 
    </body>
</html>
