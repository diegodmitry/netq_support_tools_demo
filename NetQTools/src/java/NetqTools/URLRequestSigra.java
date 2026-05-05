package NetqTools;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.security.GeneralSecurityException;
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
import java.util.ArrayList;
import java.util.List;
import javax.xml.soap.SOAPException;



/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

@WebServlet(name = "URLRequestSigra", urlPatterns = {"/URLRequestSigra"})
public class URLRequestSigra extends HttpServlet {

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
            throws ServletException, IOException, InterruptedException, GeneralSecurityException, SOAPException {
        response.setContentType("text/html;charset=UTF-8");
        
        File appJsonConfigurationFile;
        File log4jFile;
        String log4jF="";
        LoggerClass log = null;
        String jsonConfigurationFile="";
        Configuration conf = null;
        List<String> finalResult = new ArrayList<String>();
        
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
        
        String AC = request.getParameter("ac");

        String DIV = request.getParameter("div");
        String pathVar;
        
        CallSigraAC sigra = new CallSigraAC(conf, log, log4jF, AC);
        
        pathVar = getServletContext().getRealPath("/");
        
        finalResult = sigra.callSoapWebService();

        
        //result.writeTo(System.out);
        
        try (PrintWriter out = response.getWriter()) {
            
            out.println("<h5>Pedido SIGRA com AC = "+AC+" </h5>");
          
            out.println("<pre><code class=\"hljs\">"+finalResult.get(0)+"</code></pre>");
            out.println("<h5>Resposta TIBCO</h5>");
            out.println("<pre><code class=\"hljs\">"+finalResult.get(1)+"</code></pre>");
            
            
            

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
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
        } catch (GeneralSecurityException ex) {
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SOAPException ex) {
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
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
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
        } catch (GeneralSecurityException ex) {
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SOAPException ex) {
            Logger.getLogger(URLRequestSigra.class.getName()).log(Level.SEVERE, null, ex);
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
