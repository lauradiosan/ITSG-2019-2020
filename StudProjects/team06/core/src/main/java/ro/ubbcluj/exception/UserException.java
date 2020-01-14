package ro.ubbcluj.exception;

/**
 * UserException is a class which contains all the
 * exceptions regarding User Management.
 */
public class UserException extends GenericException {

    /**
     * Default constructor.
     */
    public UserException() {
        super();
    }

    /**
     * Constructor.
     *
     * @param message
     */
    public UserException(String message) {
        super("User exception: " + message);
    }

    /**
     * Constructor.
     *
     * @param message
     * @param cause
     */
    public UserException(String message, Throwable cause) {
        super("User exception: " + message, cause);
    }

}
