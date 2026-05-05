package NetqTools;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;
import com.unboundid.ldap.sdk.BindRequest;
import com.unboundid.ldap.sdk.BindResult;
import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.ResultCode;
import com.unboundid.ldap.sdk.SimpleBindRequest;
import com.unboundid.util.ssl.SSLUtil;
import com.unboundid.util.ssl.TrustAllTrustManager;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

public class Login extends HttpServlet {
    //Invalida sessao ao final de 8 horas de inatividade
    private final int MAX_INACTIVE_TIME = 8 * 60 * 60;
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
            throws ServletException, IOException {
        String catalinaBase = System.getProperty("catalina.base").replace("\\","/");
        String usrPermPath = catalinaBase + "/conf/NetQTools/usrPerm";
        String configurationJson = catalinaBase + "/conf/NetQTools/app.json";
        Configuration conf = null;
        try{
            Gson gson = new Gson();
            JsonObject jo = (JsonObject) new JsonParser().parse(new JsonReader(new FileReader(configurationJson)));
            conf = gson.fromJson(jo.getAsJsonObject("configuration"), Configuration.class);
        }catch (Exception ex){
            System.out.println("[NetqTools] - Failed to read configuration:" + ex);
        }
        GetReadeFile grf = new GetReadeFile();
        HashSet<String> usrList = grf.readFile(usrPermPath);
        response.setContentType("text/html;charset=UTF-8");
        LDAPConnection ldapConnection = null;
        try{
            //Invalida sessao ao final de 8 horas de inatividade
            if(request.getParameter("lusername") == null || request.getParameter("lpassword") == null){
                response.sendRedirect("index.jsp?authFailed=true");
            }else if(request.getParameter("lusername").equals("") || request.getParameter("lpassword").equals("")){
                response.sendRedirect("index.jsp?authFailed=true");
            }else{
                if(usrList.contains(request.getParameter("lusername"))){
                    TrustAllTrustManager tm = new TrustAllTrustManager();
                    TrustManager[] trustManagers = new TrustManager[] {tm};
                    SSLUtil sslUtil = new SSLUtil(trustManagers);
                    SSLSocketFactory socketFactory = sslUtil.createSSLSocketFactory();
                    ldapConnection = new LDAPConnection(socketFactory, conf.getLdap_server(), conf.getLdap_port(), conf.getLdap_user_dn(), conf.getLdap_user_db_password());
                    BindRequest bindRequest = new SimpleBindRequest(request.getParameter("ldomain") + "\\"+request.getParameter("lusername"), request.getParameter("lpassword"));
                    BindResult bindResult = ldapConnection.bind(bindRequest);
                    if(bindResult.getResultCode().equals(ResultCode.SUCCESS)) {
                        request.getSession().setAttribute("LOGGED_USERNAME", request.getParameter("lusername"));
                        request.getSession().setMaxInactiveInterval(this.MAX_INACTIVE_TIME);
                        createSessionCookie(request, response);
                        response.sendRedirect("menu.jsp");
                    }
                }else{
                    response.sendRedirect("index.jsp?authFailed=true");
                }
            }
        }catch(Exception ex){
            System.out.println(ex);
            response.sendRedirect("index.jsp?authFailed=true");
        }finally{
            if(ldapConnection!=null){
                if(ldapConnection.isConnected()){
                    ldapConnection.close();
                }
            }
        }
    }
    
    public void createSessionCookie(HttpServletRequest request, HttpServletResponse response) {
        Cookie[] cookies = request.getCookies();
        for (Cookie cookie : cookies) {
            if (cookie.getValue().equals(request.getSession().getId())) {
                cookie.setValue(request.getSession().getId());
                cookie.setMaxAge(this.MAX_INACTIVE_TIME);
                response.addCookie(cookie);
                break;
            }
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
//        processRequest(request, response);
            response.sendRedirect("index.jsp");
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
        processRequest(request, response);
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
