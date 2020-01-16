package ro.ubbcluj.interfaces;

import ro.ubbcluj.exception.HMSMailException;

public interface EmailService {

    void sendEmail(String email, String sendFrom, String subject, String text) throws HMSMailException;
}
