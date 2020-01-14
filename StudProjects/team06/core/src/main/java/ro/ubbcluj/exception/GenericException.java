package ro.ubbcluj.exception;

/**
 * This is a generic exception class which will be used
 * as a super class for all the exception classes.
 */
public class GenericException extends RuntimeException {

    /**
     * Default constructor.
     */
    public GenericException() {
        super();
    }

    /**
     * Constructor.
     *
     * @param message
     */
    public GenericException(String message) {
        super(message);
    }

    /**
     * Constructor.
     *
     * @param message
     * @param cause
     */
    public GenericException(String message, Throwable cause) {
        super(message, cause);
    }
}
