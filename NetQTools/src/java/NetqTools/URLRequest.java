package NetqTools;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;
import java.io.FileReader;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;



/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

@WebServlet(name = "URLRequest", urlPatterns = {"/URLRequest"})
public class URLRequest extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException, InterruptedException, GeneralSecurityException, SAXException, ParserConfigurationException {
        response.setContentType("text/html;charset=UTF-8");
        
        File appJsonConfigurationFile;
        File log4jFile;
        String log4jF="";
        LoggerClass log = null;
        String jsonConfigurationFile="";
        Configuration conf = null;
        
        String catalinaBase = System.getProperty("catalina.base").replace("\\","/");
        String log4jPath = catalinaBase+"/conf/NetQTools/log4j.xml";
        String configurationJson = catalinaBase+"/conf/NetQTools/app.json";
        
        try{
            log4jFile = new File(log4jPath);
            log4jF=log4jFile.getCanonicalPath();
            //Inicializa o logger
            log = new LoggerClass(log4jF);
            appJsonConfigurationFile= new File(configurationJson);
            jsonConfigurationFile=appJsonConfigurationFile.getCanonicalPath();
        }catch (IOException ex){
            System.out.println("Error: "+ex);
        }
        
        try{
            Gson gson = new Gson();
            JsonObject jo = (JsonObject) new JsonParser().parse(new JsonReader(new FileReader(jsonConfigurationFile)));
            conf = gson.fromJson(jo.getAsJsonObject("configuration"), Configuration.class);
        }catch (Exception ex){
            System.out.println(ex);
        }
        
        String ID = request.getParameter("id");
        String REQ = request.getParameter("req");
        String TID = request.getParameter("tid");
        String CHILD = request.getParameter("chld");
        String DIV = request.getParameter("div");
        String pathVar;
        List<String> result = new ArrayList<String>();;
        GetXmlpage gxmlp = new GetXmlpage(conf, log, log4jF);
        
        pathVar = getServletContext().getRealPath("/");
        
        result = gxmlp.requestManagement(ID, REQ, TID, CHILD);
        
        try (PrintWriter out = response.getWriter()) {
            
            if (CHILD.equals("0")){
               
                if (REQ.equals("sapa")){
                    out.println("<h5>Consulta a "+REQ+" XML2 com ID: "+result.get(0)+"</h5>");
                    out.println("<pre><code class=\"hljs\">"+result.get(1)+"</code></pre>");
                }else if(!TID.equals("NETQ")){
                    out.println("<h5>Consulta ao Pedido com o ID externo: "+result.get(0)+" ao sistema "+TID+"</h5>");
                    out.println("<pre><code class=\"hljs\">"+result.get(1)+"</code></pre>");
                }else{
                    out.println("<button id=\"btn-left\" class=\"btn-left\"><<</button>");
                    
                    out.println("<button id=\"btn-right\" class=\"btn-right\">>></button>");
                    out.println("<div class=\"grid-x grid-margin-x medium-margin-collapse\">");  
                    out.println("<div id=\"div-left\" class=\"cell small-6 large-auto\">");
                    out.println("<ul class=\"accordion\" data-accordion data-allow-all-closed=\"true\">");
                    for(int n=0;n<result.size();n = n+4){
                        out.println("<li class=\"accordion-item\" onclick=\'fillRegisto(\""+result.get(n)+"\",\"div\")\' data-accordion-item>");
                        out.println("<a href=\"#\" class=\"accordion-title\">Registo do pedido com o ID: "+result.get(n)+" - "+result.get(n+1)+"</a>");
                        out.println("<div class=\"accordion-content\" data-tab-content id=\"div"+result.get(n)+"\">");
                        out.println("</div>");
                        out.println("</li>");
                    }
                    out.println("</ul>");
                    out.println("</div>");
                    out.println("<div id=\"div-right\" class=\"cell small-6 large-auto\">");
                    out.println("<ul class=\"accordion\" data-accordion data-allow-all-closed=\"true\">");
                    for(int n=0;n<result.size();n = n+4){
                        out.println("<li class=\"accordion-item\" onclick=\'fillRegisto(\""+result.get(n)+"\",\"div_\")\' data-accordion-item>");
                        out.println("<a href=\"#\" class=\"accordion-title\">Pedidos a sistemas externos relacionado com o ID: "+result.get(n)+" - "+result.get(n+1)+"</a>");
                        out.println("<div class=\"accordion-content\" id=\"div_"+result.get(n)+"\" data-tab-content>");
                        out.println("</div>");
                        out.println("</li>");
                    }
                    out.println("</ul>");
                    out.println("</div>");
                    out.println("<input id=\"req\" value=\""+REQ+"\" type=\"hidden\">");
                    out.println("</div>");
                    out.println("<script>$(document).foundation();</script>");
                    out.println("<script>");
                    out.println("$(\"#btn-left\").click(function(){");
                    out.println("$(this).toggleClass('btn-plus');");
                    out.println("if ($(this).text() == \"<<\"){");
                    out.println("$(this).text(\">>\");");
                    out.println("}else{");
                    out.println("$(this).text(\"<<\");");
                    out.println("}");
                    out.println("$(\"#div-left\").slideToggle();");
                    out.println(" });");
                    out.println("</script>");
                    out.println("<script>");
                    out.println("$(\"#btn-right\").click(function(){");
                    out.println("$(this).toggleClass('btn-plus');");
                    out.println("if ($(this).text() == \"<<\"){");
                    out.println("$(this).text(\">>\");");
                    out.println("}else{");
                    out.println("$(this).text(\"<<\");");
                    out.println("}");
                    out.println("$(\"#div-right\").slideToggle();");
                    
                    out.println(" });");
                    out.println("</script>");
                }
            }else{
                if(DIV.equals("left")){
                    out.println("<pre><code class=\"hljs\" ID=\""+result.get(0)+"\">"+result.get(2)+"</code></pre>");
                }else{
                    out.println("<pre><code class=\"hljs\" ID=\""+result.get(0)+"\">"+result.get(1)+"</code></pre>");    
                }
            }
            
            

            /* TODO output your page here. You may use following sample code. */
            
        }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            processRequest(request, response);
        } catch (InterruptedException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (GeneralSecurityException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SAXException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ParserConfigurationException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            processRequest(request, response);
        } catch (InterruptedException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (GeneralSecurityException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SAXException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ParserConfigurationException ex) {
            Logger.getLogger(URLRequest.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
