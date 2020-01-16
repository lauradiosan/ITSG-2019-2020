package ro.ubbcluj.utils;

import org.springframework.util.ObjectUtils;
import ro.ubbcluj.exception.GenericException;

import java.util.Date;

/**
 * This class validates the application form
 */
public class ApplicationValidation {

    private static void notNull(Object object) {
        if (ObjectUtils.isEmpty(object)) {
            throw new GenericException("Please fill out the fields!");
        }
    }

    private static void dateIsValid(Date date) {
        notNull(date);

        Date currentDate = new Date();
        if (date.before(currentDate)) {
            throw new GenericException("Please insert valid dates! (as in the future)");
        }
    }

    public static void isBefore(Date startDate, Date endDate) {
        dateIsValid(startDate);
        dateIsValid(endDate);

        if (startDate.after(endDate)) {
            throw new GenericException("Please insert valid dates! (startDate < endDate)");
        }
    }
}
