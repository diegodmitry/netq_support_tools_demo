package NetqTools;

import lombok.Getter;
import lombok.Setter;

/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

@Getter @Setter
public class Configuration {
    private String mongoProd;
    private boolean mongoProdBasicAuth;
    private String mongoProdBasicAuthUser;
    private String mongoProdBasicAuthPass;
    private String auditProd;
    private boolean auditProdBasicAuth;
    private String auditProdBasicAuthUser;
    private String auditProdBasicAuthPass;
    private String mongoQA;
    private String auditQA;
    private String auxURL;
    private String auxURLaudit;
    private String sapaUrl;
    private String sigraApp;
    private String sigraCodeApp;
    private String sigraUrl;
    private String sigraAction;
    private String sigraTimeout;
    private String ldap_server;
    private int ldap_port;
    private String ldap_user_dn;
    private String ldap_user_db_password;
    
    public Configuration(){
        this.mongoProd = "";
        this.auditProd = "";
        this.mongoQA = "";
        this.auditQA = "";
        this.auxURL = "";
        this.auxURLaudit = "";
        this.sapaUrl = "";
        this.sigraApp = "";
        this.sigraCodeApp = "";
        this.sigraUrl = "";
        this.sigraAction = "";
        this.sigraTimeout = "";
        this.ldap_server = "";
        this.ldap_port = -1;
        this.ldap_user_dn  = "";
        this.ldap_user_db_password = "";
    }   
}