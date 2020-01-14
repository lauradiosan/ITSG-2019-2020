package ro.ubbcluj.util;

import ro.ubbcluj.exception.GenericException;

import java.util.Date;

/**
 * ValidationUtil class checks if an object is null and returns an exception if the statement is true.
 */
public class ValidationUtil {

    public static void invalidDate(Date startDate, Date endDate) {
        if (startDate.after(endDate)) {
            throw new GenericException("Start date after end date");
        }
    }

    public static void notNull(Object object) {
        if (object == null) {
            throw new GenericException("Invalid" + object.getClass().toString() + "parameter");
        }
    }

}
