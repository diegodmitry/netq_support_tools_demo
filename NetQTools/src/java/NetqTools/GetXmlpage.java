package NetqTools;

/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.io.Writer;
import static java.lang.Boolean.FALSE;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.util.EntityUtils;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.xml.serialize.OutputFormat;
import org.apache.xml.serialize.XMLSerializer;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

public class GetXmlpage {
    
    LoggerClass log = null;
    Configuration conf = null;
    String log4jF="";
    
    public GetXmlpage(Configuration conf, LoggerClass log, String log4jF){
        this.log = log;
        this.conf = conf;
        this.log4jF = log4jF;
    }
    
    public List<String> getTestInfo(String url, boolean useBasicAuth, String basicAuthUser, String basicAuthPass, int submitId, String id, String chld) throws IOException, InterruptedException, GeneralSecurityException, SAXException, ParserConfigurationException{
       
       
        String responseBody="";
        List<String> rOrders = new ArrayList<>();
        String oType="";
        String replace="";
        String replace1="";
        String replace2="";
        String replace3="";
        List<String> finalResult = new ArrayList<>();
        String regex= "";
        String rText= "";
        String mText= "";
        
        CloseableHttpClient httpclient;

        if(useBasicAuth){
            CredentialsProvider provider = new BasicCredentialsProvider();
            provider.setCredentials(
                AuthScope.ANY,
                new UsernamePasswordCredentials(basicAuthUser, basicAuthPass)
            );
            httpclient = HttpClientBuilder.create().setDefaultCredentialsProvider(provider).build();
        }else{
            httpclient = HttpClientBuilder.create().build();
        }

        try {
            HttpGet httpget = new HttpGet(url); 

            //System.out.println("Executing request " + httpget.getRequestLine());

            // Create a custom response handler
            ResponseHandler<String> responseHandler = new ResponseHandler<String>() {

                @Override
                public String handleResponse(final HttpResponse response) throws ClientProtocolException, IOException {
                    int status = response.getStatusLine().getStatusCode();
                    if (status >= 200 && status < 300) {
                        HttpEntity entity = response.getEntity();
                        return entity != null ? EntityUtils.toString(entity) : null;
                    } else {
                        throw new ClientProtocolException("Unexpected response status: " + status);
                    }
                }

            };
            responseBody = httpclient.execute(httpget, responseHandler);
            
            if (submitId == 1 && chld.equals("0")){
                // Devolve lista de pedidos filhos
                rOrders = relatedOrders(responseBody,id);
                // Devolve o tipo do teste
                oType = orderType(responseBody);
            }
            
            String xmlResponse = this.format(responseBody,FALSE);

            replace = xmlResponse.replace("&lt;","<");
            // Coloca "/n" no xml
            //sb = xmlFormat(replace);

            replace1 = replace.replace("<", "&lt;");
            replace2 = replace1.replace("&#xd;", "");
            // Remove white Lines
            replace3 = replace2.replaceAll("(?m)^[ \t]*\r?\n", "");
            
        } finally {
            httpclient.close();
        }
        
        
        finalResult.add(replace3);
        //System.out.println(finalResult.get(0));
        //System.out.println("submitId = "+submitId);
        if (submitId == 1){
            finalResult.add(oType);
            for(int n=0; n < rOrders.size(); n++){
                //System.out.println(n+" -> "+rOrders.get(n));
                finalResult.add(rOrders.get(n));
                //System.out.println(n+" -> "+finalResult.get(n+1));
            }
        }
       
        return finalResult;
    }
    
    public List<String> relatedOrders(String responseBody, String id){
        List<String> rOrders = new ArrayList<>();
        int i = 0;
        String regex = "";
        String mText = "";
        
        regex = "<order><id>([\\w\\-]+)</id>";
        Pattern p = Pattern.compile(regex);
        Matcher m = p.matcher(responseBody);

        while (m.find()) {
            mText = m.group().substring(11,m.group().length()-5);
            //System.out.println("i = "+i);
            if (!mText.equals(id)){
                rOrders.add(mText);      
                //System.out.println("related orders "+i+": "+rOrders.get(i));
                i++;
            }
        }
        
        return rOrders;
    }
    
    public String orderType(String responseBody){
        String oType = "";
        String regex = "";
        
        regex = "^.+?<orderType>(.+?)</orderType>.+?priority.+$";
        Pattern p = Pattern.compile(regex,Pattern.MULTILINE);
        Matcher m = p.matcher(responseBody);
        if(m.find()){
            oType = m.group(1);
        }else{
            oType = "COCO";
        }
        
        //System.out.println("orderType: "+oType);
        
        return oType;
    }
    
    public StringBuffer xmlFormat(String responseBody){
        StringBuffer sb = new StringBuffer();
        String regex = "";
        String mText = "";
        String rText = "";
        
        regex = "</[\\w\\:]+>";
        Pattern p = Pattern.compile(regex);
        Matcher m = p.matcher(responseBody);

        while (m.find()) {
            mText = m.group();
            rText = mText + "\n";
            //System.out.println(mText);
            m.appendReplacement(sb, rText);
        }
        m.appendTail(sb);
        
        return sb;
    }
    
    public List<String> requestManagement(String id,String req,String tid,String chld) throws IOException, InterruptedException, GeneralSecurityException, SAXException, ParserConfigurationException{
        
        String request1 = "";
        String request2 = "";
        List<String> response = new ArrayList<>();
        List<String> response1;
        List<String> response2;
        List<String> idList = new ArrayList<>();
        
        switch (req) {
            case "prodMongo":
                if(tid.equals("NETQ")){
                    request1 = this.conf.getAuditProd()+id+this.conf.getAuxURLaudit();
                    response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                    request2 = this.conf.getMongoProd()+id+this.conf.getAuxURL();
                    response2 = getTestInfo(request2, this.conf.isMongoProdBasicAuth(),this.conf.getMongoProdBasicAuthUser(),this.conf.getMongoProdBasicAuthPass(), 1, id, chld);
                    response.add(id);
                    if (chld.equals("0")){
                        response.add(response2.get(1));
                    }
                    response.add(response1.get(0));
                    response.add(response2.get(0));
                    if (chld.equals("0")){
                        for(int n=2; n < response2.size(); n++){
                            //System.out.println("Lista inicial elemento "+n+": "+response2.get(n));
                            idList.add(response2.get(n));
                        }
                        while(!idList.isEmpty()){
                            id = idList.get(0);
                            //System.out.println("ID a usar: "+id);
                            request1 = this.conf.getAuditProd()+id+this.conf.getAuxURLaudit();
                            response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                            request2 = this.conf.getMongoProd()+id+this.conf.getAuxURL();
                            response2 = getTestInfo(request2, this.conf.isMongoProdBasicAuth(),this.conf.getMongoProdBasicAuthUser(),this.conf.getMongoProdBasicAuthPass(), 1, id, chld);
                            response.add(id);
                            response.add(response2.get(1));
                            response.add(response1.get(0));
                            response.add(response2.get(0));
                            idList.remove(0);
                            //System.out.println("tamanho da lista: "+response2.size());
                            for(int n=2; n < response2.size(); n++){
                                //System.out.println("add to list elemnto "+n+": "+response2.get(n));
                                idList.add(0,response2.get(n));
                            }
                        }
                    }
                }else{
                    request1 = this.conf.getAuditProd()+tid+"/"+id;
                    response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                    response.add(id);
                    response.add(response1.get(0));
                }
                break;
            case "qaMongo":
                //System.out.println("TipoID: " + tid);
                if(tid.equals("NETQ")){
                    request1 = this.conf.getAuditQA()+id+this.conf.getAuxURLaudit();
                    response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                    request2 = this.conf.getMongoQA()+id+this.conf.getAuxURL();
                    //System.out.println("URL QA: "+request2);
                    response2 = getTestInfo(request2, this.conf.isMongoProdBasicAuth(),this.conf.getMongoProdBasicAuthUser(),this.conf.getMongoProdBasicAuthPass(), 1, id, chld);
                    response.add(id);
                    if (chld.equals("0")){
                        response.add(response2.get(1));
                    }
                    response.add(response1.get(0));
                    response.add(response2.get(0));
                    if (chld.equals("0")){
                        for(int n=2; n < response2.size(); n++){
                            //System.out.println("Lista inicial elemento "+n+": "+response2.get(n));
                            idList.add(response2.get(n));
                        }
                        while(!idList.isEmpty()){
                            id = idList.get(0);
                            //System.out.println("ID a usar: "+id);
                            request1 = this.conf.getAuditQA()+id+this.conf.getAuxURLaudit();
                            response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                            request2 = this.conf.getMongoQA()+id+this.conf.getAuxURL();
                            //System.out.println("URL QA: "+request2);
                            response2 = getTestInfo(request2, this.conf.isMongoProdBasicAuth(),this.conf.getMongoProdBasicAuthUser(),this.conf.getMongoProdBasicAuthPass(), 1, id, chld);
                            response.add(id);
                            response.add(response2.get(1));
                            response.add(response1.get(0));
                            response.add(response2.get(0));
                            idList.remove(0);
                            //System.out.println("tamanho da lista: "+response2.size());
                            for(int n=2; n < response2.size(); n++){
                                //System.out.println("add to list elemnto "+n+": "+response2.get(n));
                                idList.add(0,response2.get(n));
                            }
                        }
                    }
                }else{
                    request1 = this.conf.getAuditQA()+tid+"/"+id.replace("#", "%23");
                    response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                    response.add(id);
                    response.add(response1.get(0));
                }
                break;
            case "sapa":
                //System.out.println("SAPA "+this.conf.getSapaUrl());
                request1 = this.conf.getSapaUrl()+id;
                response1 = getTestInfo(request1, this.conf.isAuditProdBasicAuth(),this.conf.getAuditProdBasicAuthUser(),this.conf.getAuditProdBasicAuthPass(), 0, id, chld);
                response.add(id);
                response.add(response1.get(0));
                break;
            
        }
        return response;
    }
    
    public String format(String xml, Boolean ommitXmlDeclaration) throws IOException, SAXException, ParserConfigurationException {
          
        DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = db.parse(new InputSource(new StringReader(xml)));
          
        OutputFormat format = new OutputFormat(doc);
        format.setIndenting(true);
        format.setIndent(2);
        format.setOmitXMLDeclaration(ommitXmlDeclaration);
        format.setLineWidth(Integer.MAX_VALUE);
        Writer outxml = new StringWriter();
        XMLSerializer serializer = new XMLSerializer(outxml, format);
        serializer.serialize(doc);
          
        return outxml.toString();
          
    }

}
