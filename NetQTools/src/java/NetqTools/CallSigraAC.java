package NetqTools;

/**
 *
 * @author calvin
 */


import java.io.ByteArrayOutputStream;
import java.security.GeneralSecurityException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;


import javax.xml.namespace.QName;
import javax.xml.soap.MessageFactory;
import javax.xml.soap.MimeHeaders;
import javax.xml.soap.SOAPBody;
import javax.xml.soap.SOAPConnection;
import javax.xml.soap.SOAPConnectionFactory;
import javax.xml.soap.SOAPElement;
import javax.xml.soap.SOAPEnvelope;
import javax.xml.soap.SOAPException;
import javax.xml.soap.SOAPHeader;
import javax.xml.soap.SOAPHeaderElement;
import javax.xml.soap.SOAPMessage;
import javax.xml.soap.SOAPPart;

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.io.Writer;
import static java.lang.Boolean.FALSE;
import java.util.ArrayList;
import java.util.List;
 
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
 
import org.apache.xml.serialize.OutputFormat;
import org.apache.xml.serialize.XMLSerializer;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;




public class CallSigraAC {
    
    LoggerClass log = null;
    Configuration conf = null;
    String log4jF="";
    String sigraUrl="";
    String ac="";
    
    public CallSigraAC(Configuration conf, LoggerClass log, String log4jF, String ac){
        this.log = log;
        this.conf = conf;
        this.log4jF = log4jF;
        this.sigraUrl = this.conf.getSigraUrl();
        this.ac = ac;
    }
    
    public List<String> callSoapWebService()throws  IOException, InterruptedException, GeneralSecurityException{
       
        SOAPMessage soapRespeonse = null;
        String response = null;
        String request = null;
        String request2 = null;
        List<String> finalResult = new ArrayList<>();
        
        try{
            // Create SOAP Connection
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();

            //Send SOAP Message to SOAP server
            SOAPMessage smessage = createSOAPRequest();
  
            request = this.soapMessageToString(smessage);
            request2 = this.format(request,FALSE);
            
            String rep = request2.replace("&lt;","<");        
            
            String rep1 = rep.toString().replace("<", "&lt;");
            String rep2 = rep1.replace("&#xd;", "");
            // Remove white Lines
            String rep3 = rep2.replaceAll("(?m)^[ \t]*\r?\n", "");
            
            System.out.println(rep3);
            
            finalResult.add(rep3);
            
            System.out.println(finalResult.get(0));
            
            soapRespeonse = soapConnection.call(smessage,this.sigraUrl);

            //System.out.println(this.soapMessageToString(soapRespeonse));
            response = this.soapMessageToString(soapRespeonse);
            response = this.format(response,FALSE);
            
            String replace = response.replace("&lt;","<");        
            
            String replace1 = replace.toString().replace("<", "&lt;");
            String replace2 = replace1.replace("&#xd;", "");
            // Remove white Lines
            String replace3 = replace2.replaceAll("(?m)^[ \t]*\r?\n", "");
            
            finalResult.add(replace3);
            
        }catch (Exception e) {
            System.err.println("\nError occurred while sending SOAP Request to Server!\nMake sure you have the correct endpoint URL and SOAPAction!\n");
            e.printStackTrace();
        }
        System.out.println(response);
        return finalResult;
    }
    
    public SOAPMessage createSOAPRequest() throws  IOException, InterruptedException, GeneralSecurityException, SOAPException{
        
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage soapMessage = messageFactory.createMessage();
        
        createSoapEnvelope(soapMessage);

        MimeHeaders headers = soapMessage.getMimeHeaders();
        headers.addHeader("SOAPAction", this.conf.getSigraAction());

        soapMessage.saveChanges();

        /* Print the request message, just for debugging purposes */
        //System.out.println("Request SOAP Message:");
        //soapMessage.writeTo(System.out);
        //System.out.println("\n");

        return soapMessage;
    }
    
    public void createSoapEnvelope(SOAPMessage soapMessage)throws IOException, InterruptedException, GeneralSecurityException, SOAPException{
        
        
        SOAPPart soapPart = soapMessage.getSOAPPart();
        
        // SOAP Envelope
        SOAPEnvelope envelope = soapPart.getEnvelope();

        // SOAP Xmnls Declarations
        //envelope.addNamespaceDeclaration("soapenv", "http://schemas.xmlsoap.org/soap/envelope/");
        SOAPElement soapEL = envelope.addNamespaceDeclaration("soap", "urn://ptp.pt/SharedResources/SchemaDefinitions/EAIMessaging/SOAPHeader");
        envelope.addNamespaceDeclaration("_dat", "urn://ptp.pt/BusinessDomains/RESOURCE/ResourceNetwork/1.0/getNetworkInformation/_Data");
        envelope.addNamespaceDeclaration("get", "urn://ptp.pt/IntegrationDataModel/ResourceNetwork/1.0/getNetworkInformation");


        // SOAP Header
        SOAPHeader header = soapMessage.getSOAPHeader();
       
        QName qname1 = header.createQName("HeaderRequest", "soap");
        QName qname2 = header.createQName("npu", "soap");
        QName qname3 = header.createQName("creationTime", "soap");
        QName qname4 = header.createQName("timeout", "soap");
        QName qname5 = header.createQName("Credentials", "soap");
        QName qname6 = header.createQName("systemCode", "soap");
       
        SOAPHeaderElement soapHeaderE1 = header.addHeaderElement(qname1);
        SOAPElement soapHeaderE2 = soapHeaderE1.addChildElement(qname2);
        soapHeaderE2.addTextNode(this.npuCalc());
        SOAPElement soapHeaderE3 = soapHeaderE1.addChildElement(qname3);
        soapHeaderE3.addTextNode(this.createTime());
        SOAPElement soapHeaderE4 = soapHeaderE1.addChildElement(qname4);
        soapHeaderE4.addTextNode(this.conf.getSigraTimeout());
        SOAPElement soapHeaderE5 = soapHeaderE1.addChildElement(qname5);
        SOAPElement soapHeaderE6 = soapHeaderE5.addChildElement(qname6);
        soapHeaderE6.addTextNode(this.conf.getSigraCodeApp());


        // SOAP Body
        SOAPBody soapBody = envelope.getBody();
        SOAPElement soapElement = soapBody.addChildElement("DataInput", "_dat");
        SOAPElement soapElement1 = soapElement.addChildElement("getNetworkInformationInput", "get");
        SOAPElement soapElement2 = soapElement1.addChildElement("ParametrosOperacao", "get");
        SOAPElement soapElement3 = soapElement2.addChildElement("DataOperacao", "get"); 
        soapElement3.addTextNode(this.createTime());
        SOAPElement soapElement4 = soapElement2.addChildElement("PedidoInformacao", "get");
        SOAPElement soapElement5 = soapElement4.addChildElement("Accao", "get"); 
        soapElement5.addTextNode("2");
        SOAPElement soapElement6 = soapElement4.addChildElement("AreaCentral", "get"); 
        soapElement6.addTextNode(this.ac);
        SOAPElement soapElement7 = soapElement4.addChildElement("Aplicacao", "get"); 
        soapElement7.addTextNode(this.conf.getSigraApp());
    }
    
    public String npuCalc(){
        String npu = "";
        
        Date d = new Date();
        SimpleDateFormat masc = new SimpleDateFormat("yyyyMMddHHmmss");
        String now = masc.format(d);
        npu = "0099F1671V1_0xx"+now+"990000000482939482000";
        return npu;
    }
    
    public String createTime(){
        String ctime = "";
        Date d = new Date(System.nanoTime());
        SimpleDateFormat masc = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSSSXXX");
        masc.setTimeZone(TimeZone.getTimeZone("CET"));
        String now = masc.format(d);
        ctime = now;
        return ctime;
    }
    
    public String soapMessageToString(SOAPMessage message) 
    {
        String result = null;

        if (message != null) 
        {
            ByteArrayOutputStream baos = null;
            try 
            {
                baos = new ByteArrayOutputStream();
                message.writeTo(baos); 
                result = baos.toString();
            } 
            catch (Exception e) 
            {
            } 
            finally 
            {
                if (baos != null) 
                {
                    try 
                    {
                        baos.close();
                    } 
                    catch (IOException ioe) 
                    {
                    }
                }
            }
        }
        return result;
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
