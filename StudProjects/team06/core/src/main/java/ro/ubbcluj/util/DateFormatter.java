package ro.ubbcluj.util;

import lombok.extern.slf4j.Slf4j;
import ro.ubbcluj.exception.GenericException;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * This class formats dates
 */
@Slf4j
public class DateFormatter {
    public static Date getDate(String dateInString) {
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat();
        simpleDateFormat.applyPattern("MM/dd/yyyy");

        try {
            return simpleDateFormat.parse(dateInString);
        } catch (ParseException e) {
            log.error("DateFormatterError: " + e.getLocalizedMessage());
            throw new GenericException("DateFormatter: " + e.getLocalizedMessage());
        }
    }
}
