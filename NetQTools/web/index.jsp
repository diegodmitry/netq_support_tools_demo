<%-- 
    Document   : index
    Created on : Jul 18, 2018, 6:12:11 PM
    Author     : Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
--%>
<%
    if(request.getSession().getAttribute("LOGGED_USERNAME")!=null){
        response.sendRedirect("netqLogs.jsp");
    }
%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Netq Support tools</title>
        <%@include file="cssInclude.jsp" %>
    </head>
    <body class="login_bckg">
        <div class="row"> 
            <%if(request.getParameter("authFailed")!=null && request.getParameter("authFailed").equals("true")){%>
            <div class="translucent-form-overlay-erro callout" id="errologin" data-closable>
                <p>ERRO NA AUTENTICAÇÃO !!!</p>
                <button class="close-button" aria-label="Dismiss alert" type="button" data-close>
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <%}%>
            <div class="translucent-form-overlay cell medium-4 medium-cell-block" id="login">
                <form id="flogin" action="login.do" method="post">
                    <h3>signup</h3>
                    <div class="row columns">
                        <label>Domain
                            <select name="ldomain" id="ldomain">
                                <option value="ptportugal" selected="selected">PTPORTUGAL</option>
                                <option value="ptc">PTC</option>
                                <option value="ptcom">PTCOM</option>
                                <option value="ptin">PTIN</option>
                                <option value="ptsi">PTSI</option>
                                <option value="tmn">TMN</option>
                              </select>
                        </label>
                    </div>
                    <div class="row columns">
                        <label>Username:
                            <input type="text" name="lusername" id="lusername" size="30" placeholder="username">
                        </label>
                    </div>
                    <div class="row columns">
                        <label>Password
                            <input type="password" name="lpassword" id="lpassword" size="30">
                        </label>
                        <input type="submit" value="login" class="secondary button expanded search-button">
                    </div>
                </form> 
            </div>        
        </div>
        <%@include file="jsInclude.jsp" %>
    </body>
</html>
