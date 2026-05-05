package NetqTools;

import java.io.File;
import java.io.FileInputStream;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.apache.commons.lang3.exception.ExceptionUtils;

/**
 *
 * @author Augusto Fonseca | augusto-f-fonseca@telecom.pt
 */

public class Utils {
    
    public static void writeConsoleWithDate(String text){
       Date d = new Date();
       SimpleDateFormat masc = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss,SSS");
       String now = masc.format(d);
       System.out.println(now+" - "+text);
    }
    
    public static boolean renameFileWithLock(File source,File destination) throws Exception{
        boolean renSucess=false;
        RandomAccessFile fileDestinationLocked = null; 
        FileLock fileLock = null;
        FileChannel fileChannel=null;
        destination.delete();
        try{
            fileDestinationLocked =  new RandomAccessFile(destination,"rw");
            fileChannel = fileDestinationLocked.getChannel();
            fileLock = fileChannel.lock();
            if(fileLock != null){
                 byte[] b = new byte[(int) source.length()];
                 FileInputStream fileInputStream = new FileInputStream(source);
                 fileInputStream.read(b);
                 fileInputStream.close();
                 ByteBuffer buf = ByteBuffer.wrap(b);
                 fileChannel.write(buf);
            }
            renSucess=true;
            source.delete();
        }finally{
            if(fileLock != null){
                fileLock.release();
            }
            if(fileChannel!=null){
                fileChannel.close();
            }
            if(fileDestinationLocked!=null){
               fileDestinationLocked.close(); 
            }
        }
        return renSucess;
    }
    
    public static boolean checkIfCanReadAndWrite(String filePath){
        boolean canReadAndWrite=false;
        File f = new File(filePath);
        RandomAccessFile file = null; 
        FileLock fileLock = null;
        FileChannel fileChannel=null;
        try{
            file =  new RandomAccessFile(f,"rw");
            fileChannel = file.getChannel();
            fileLock = fileChannel.tryLock();
            if(fileLock != null){
                canReadAndWrite=true;
            }
        }catch(Exception ex){
        }finally{
            if(fileLock != null){
                try{
                    fileLock.release();
                    if(fileChannel!=null){
                        fileChannel.close();
                    }
                }catch(Exception ex){
                }
            }  
        }
        return canReadAndWrite;
    }
    
    public static String getStackTrace(Throwable throwable){
        return ExceptionUtils.getStackTrace(throwable);
    }
    
    public static void doSleep(long miliseconds){
        try{Thread.sleep(miliseconds);}catch(Exception ex){}
    }
    
    public static String getTime(long t){
        String format = String.format("%%0%dd", 2);
        t = t / 1000;
        String seconds = String.format(format, t % 60);
        String minutes = String.format(format, (t % 3600) / 60);
        String hours = String.format(format, t / 3600);
        return hours+"h:"+minutes+"m:"+seconds+"s";
    }
}
