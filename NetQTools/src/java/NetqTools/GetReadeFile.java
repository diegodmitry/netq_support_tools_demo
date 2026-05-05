package NetqTools;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import org.apache.commons.io.FileUtils;

/**
 *
 * @author Pedro Jose Correia Alves dos Reis (pedro-j-reis@telecom.pt)
 */

public class GetReadeFile {
    
    private LoggerClass log;
    private String logger;
    
    public GetReadeFile(LoggerClass log,String logger){
        this.log=log;
        this.logger=logger;
    }
    
    public GetReadeFile(){
    }
    
    public HashSet<String> readFile(String filename){
        try{
            String [] linesReaded = FileUtils.readFileToString(new File(filename), "UTF-8").split("\n");
            return new HashSet<>(new ArrayList<>(Arrays.asList(linesReaded)));
        }catch (Exception ex){
            //this.log.error("Found exception:"+ex, this.logger);
            System.out.println("[NetqTools] - Failed to read file '" + filename + "': " + ex);
            return null;
        }
    }
}
