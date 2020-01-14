package ro.ubbcluj.utils;

import org.springframework.security.core.context.SecurityContextHolder;

public class User {

    /**
     * Method used to get the username from the current logged in user
     *
     * @return
     */
    public static String getCurrentUserName() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}
