package ro.ubbcluj.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.NoHandlerFoundException;
import ro.ubbcluj.exception.GenericException;

/**
 * This class handles the errors from all the controllers
 */
@ControllerAdvice
public class ErrorController {
    private static Logger logger = LoggerFactory.getLogger(ErrorController.class);

    /**
     * Manages errors from Spring Security
     *
     * @param throwable
     * @param model
     * @return
     */
    @ExceptionHandler(Throwable.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public String exception(final Throwable throwable, final Model model) {
        logger.error("Exception during execution of SpringSecurity application", throwable);
        String errorMessage = (throwable != null ? throwable.getMessage() : "Unknown error");
        model.addAttribute("errorMessage", errorMessage);
        return "error";
    }

    /**
     * @param ex
     * @return
     */
    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ExceptionHandler(NoHandlerFoundException.class)
    public String handle(Exception ex) {
        return "error";
    }

    /**
     * @param exception
     * @param model
     * @return
     */
    @ExceptionHandler(GenericException.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public String handleGenericException(final GenericException exception, final Model model) {
        model.addAttribute("errorMessage", exception.getMessage());
        return "error";
    }

}
