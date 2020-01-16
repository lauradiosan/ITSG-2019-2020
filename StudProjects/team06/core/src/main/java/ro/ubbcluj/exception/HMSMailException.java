package ro.ubbcluj.exception;

import javax.mail.MessagingException;

/**
 * This class contains all the exceptions regarding mails
 */
public class HMSMailException extends MessagingException {

    /**
     * Default constructor.
     */
    public HMSMailException() {
        super();
    }

    /**
     * Constructor.
     *
     * @param message
     */
    public HMSMailException(String message) {
        super("Room exception: " + message);
    }

}
