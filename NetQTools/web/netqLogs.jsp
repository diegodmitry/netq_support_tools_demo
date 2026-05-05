<%-- 
    Document   : index
    Created on : Mar 29, 2018, 3:34:50 PM
    Author     : Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
--%>
<%@ taglib uri = "http://java.sun.com/jsp/jstl/functions" prefix = "fn" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@page import="java.io.IOException"%>
<%@page import="NetqTools.GetXmlpage" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page trimDirectiveWhitespaces="true"%> 


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
                            Ambiente
                            <select class="app_select" id="amb">
                                <option value="prodMongo">Producao</option>
                                <option value="qaMongo">QA</option>
                            </select>
                            Tipo ID
                            <select class="app_select" id="tipoid">
                                <option value="NETQ">NetQ</option>
                                <option value="TIBCO">TIBCO(NPU)</option>
                                <option value="NETWIN">NETWIN(NPU)</option>
                                <option value="SIGRA">SIGRA(NPU)</option>
                                <option value="NA">NA(OPK)</option>
                            </select>
                            ID
                            <input class="app_input" type="text" id="submitID" placeholder="mongo ID"/>
                        </li>
                        <li>
                            <button type="submit" class="hollow button secondary " onclick="sendRequest()">submit</button>
                        </li>

                    </ul>
                </div>
                <div class="top-bar-right">
                    <ul class="menu text_menu">
                        <li>
                            SAPA ID
                            <input class="app_input" type="text" id="sapaID" placeholder="SAPA ID"/>
                        </li>
                        <li>
                            <button type="submit" class="hollow button secondary" onclick="sendID('sapa','sapa')">submit</button>
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
