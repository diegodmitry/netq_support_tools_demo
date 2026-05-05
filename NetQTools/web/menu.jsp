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

<%
    if(request.getSession().getAttribute("LOGGED_USERNAME")==null){
        response.sendRedirect("index.jsp");
    }
%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Netq Support tools</title>
        <%@include file="cssInclude.jsp" %>
        
    </head>
    <body>
        <div class="top-bar backgroud_black">
            <div class="top-bar-left backgroud_black">
                <ul class="menu text_menu backgroud_black">
                    <li>
                        <button type="button" class="menu-icon link_app" data-toggle="offCanvas"></button>
                    </li>
                    <li>       
                        <a target="Altice" href="http://www.altice.pt" class="link_app">
                            &nbsp;&nbsp;&nbsp;<img src= "images/altice_logo_invert.jpg" width="25" height="25">
                        </a>
                    </li>
                    <tab2></tab2>
                    <li class="backgroud_black">
                        <h5 class="backgroud_black">NetQ Support Tools</h5>
                    </li>                    
                </ul>
            </div>
            <div class="top-bar-right backgroud_black">
                <ul class="menu text_menu backgroud_black">
                    <li><a class="hollow button tri" href="logout.do"><%=request.getSession().getAttribute("LOGGED_USERNAME")%> Logout</a></li>
                </ul>
            </div>
        </div>
                <div class="off-canvas-wrapper">
        <div class="off-canvas position-esq backgroud_black" id="offCanvas" data-off-canvas>
            <button class="close-button" aria-label="Close menu" type="button" data-close>
                <span aria-hidden="true">&times;</span>
            </button>
            <h5 class="backgroud_black">MENU</h5><br>
            <ul class="menu vertical text_menu backgroud_black   ">    
                <li><a class="hollow button esq" href="#" id="audit">Audit Logs</a></li>
                <li><a class="hollow button esq" href="#" id="sigra">Pedidos a SIGRA</a></li>

              </ul>
        </div>
        <div class="off-canvas-content" data-off-canvas-content>           
            <div id="content"></div>
        </div>
       
        <%@include file="jsInclude.jsp" %>
        <script>
            var stayAlive = function () {
                $.ajax("doPing.do?ping=" + new Date().getTime())
                    .always(function (datajqXHR, textStatus, jqXHRerrorThrown) { });
            };
            stayAlive();
            window.setInterval(stayAlive, 300000);
         
            $(document).ready(function() {
                $(document).foundation();
            })
            
            $(document).ready( function() {
                $("#audit").on("click", function() {
                    $("#content").load("netqLogs.jsp");
                });               
            });
            
            $(document).ready( function() {
                $("#sigra").on("click", function() {
                    $("#content").load("sigra.jsp");
                });               
            });
        </script>
        
    </body>
</html>
