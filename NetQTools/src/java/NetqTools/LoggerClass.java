package NetqTools;

import java.io.File;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.LoggerContext;
import org.apache.logging.log4j.status.StatusLogger;

/**
 *
 * @author Augusto Fonseca | augusto-f-fonseca@telecom.pt
 * 
 * |-----------------------------------------|
 * |           Standard Log Levels           |
 * |-----------------------------------------|
 * | Standard Level   |  intLevel            |
 * | OFF              |  0                   |
 * | FATAL            |  100                 |
 * | ERROR            |  200                 |
 * | WARN             |  300                 |
 * | INFO             |  400                 |
 * | DEBUG            |  500                 |
 * | TRACE            |  600                 |
 * | ALL              |  Integer.MAX_VALUE   |
 * |-----------------------------------------|
 * 
 */
public class LoggerClass {
    private Logger logger;
    private String configurationFile;
    private final int FATAL = 100;
    private final int ERROR = 200;
    private final int WARN = 300;
    private final int INFO = 400;
    private final int DEBUG = 500;
    private final int TRACE = 600;

    public LoggerClass(String configurationFile){
        //System.setProperty("log4j2.debug", "true");
        try{
            this.configurationFile=configurationFile;
            StatusLogger.getLogger().setLevel(org.apache.logging.log4j.Level.OFF);
            LoggerContext context = (LoggerContext) LogManager.getContext(false);
            File configurationF = new File(this.configurationFile);
            context.setConfigLocation(configurationF.toURI());
        }catch(Exception ex){
            System.out.println("Error on log4j configuration file: "+this.configurationFile+": "+Utils.getStackTrace(ex));
        }
    } 
    
    public void write(Level level,String logContent,String logger){
        this.logger = LogManager.getLogger(logger);
        switch (level.intLevel()){
            case FATAL:   
                this.logger.fatal(logContent);
                break;
            case ERROR:
                this.logger.error(logContent);
                break;
            case WARN:
                this.logger.warn(logContent);
                break;
            case INFO:
                this.logger.info(logContent);
                break;
            case DEBUG:
                this.logger.debug(logContent);
                break;
            case TRACE:
                this.logger.trace(logContent);
                break;
            default:
                break;
        }
    }
    
    public void write(Level level,String logContent,Throwable throwable,String logger){
        this.logger = LogManager.getLogger(logger);
        switch (level.intLevel()){
            case FATAL:   
                this.logger.fatal(logContent,throwable);
                break;
            case ERROR:
                this.logger.error(logContent,throwable);
                break;
            case WARN:
                this.logger.warn(logContent,throwable);
                break;
            case INFO:
                this.logger.info(logContent,throwable);
                break;
            case DEBUG:
                this.logger.debug(logContent,throwable);
                break;
            case TRACE:
                this.logger.trace(logContent,throwable);
                break;
            default:
                break;
        }
    }
    
    public void fatal(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.fatal(logContent);
    }
    
    public void fatal(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.fatal(logContent,throwable);
    }
    
    public void error(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.error(logContent);
    }
    
    public void error(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.error(logContent,throwable);
    }
    
    public void warn(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.warn(logContent);
    }
    
    public void warn(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.warn(logContent,throwable);
    }
    
    public void info(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.info(logContent);
    }
    
    public void info(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.info(logContent,throwable);
    }
       
    public void debug(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.debug(logContent);
    }
    
    public void debug(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.debug(logContent,throwable);
    }
    
    public void trace(String logContent,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.trace(logContent);
    }
    
    public void trace(String logContent,Throwable throwable,String logLogger){
        this.logger = LogManager.getLogger(logLogger);
        this.logger.trace(logContent,throwable);
    }
    
    /**
     * @return the logger
     */
    public Logger getLogger() {
        return logger;
    }

    /**
     * @param logger the logger to set
     */
    public void setLogger(Logger logger) {
        this.logger = logger;
    }
}