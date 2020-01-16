package ro.ubbcluj.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.ObjectUtils;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import ro.ubbcluj.interfaces.UserService;
import ro.ubbcluj.model.frontObjects.LoginPurposes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * This class controls the login and register page and updates the view whenever data changes
 */

@Slf4j
@Controller
public class IndexController {
    private static final String ANNOUNCEMENT_EMAIL = "applicationsystem802@gmail.com";
    private static final String SUBJECT = "Registration confirmation";
    private static final String TEXT = "Your account has been successfully created!";
    @Autowired
    private UserService userService;

    /**
     * Method used to redirect to the index page.
     *
     * @return
     */
    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String index(@ModelAttribute(value = "loginPurposes") LoginPurposes loginPurposes,
                        Model model) {
        System.out.println("aiciiii");
        System.out.println(loginPurposes);
        if (ObjectUtils.isEmpty(loginPurposes)) {
            model.addAttribute("loginPurposes", new LoginPurposes());
        } else {
            model.addAttribute("loginPurposes", loginPurposes);
        }
        return "index";
    }

    /**
     * Method used to log in the user.
     *
     * @param model
     * @param error
     * @param logout
     * @return
     */
    @RequestMapping(value = "/login", method = RequestMethod.GET)
    public String login(@ModelAttribute(value = "loginPurposes") LoginPurposes loginPurposes,
                        Model model, String error, String logout) {
        System.out.println("suntem pe /login");
        if (error != null) {
            log.error("Your username and password is invalid.");
            String message = "Invalid username or password, try again !";
            model.addAttribute("message", message);
        }
        if (logout != null)
            log.info("You have been logged out successfully.");

        if (ObjectUtils.isEmpty(loginPurposes)) {
            model.addAttribute("loginPurposes", new LoginPurposes());
        } else {
            model.addAttribute("loginPurposes", loginPurposes);
        }
        return "index";
    }

    /**
     * Method used to redirect to the access denied page
     *
     * @return
     */
    @RequestMapping(value = "/accessDenied", method = RequestMethod.GET)
    public String accessDenied() {
        return "/accessDenied";
    }

    /**
     * Method used to redirect to duplicate username error page
     *
     * @return
     */
    @RequestMapping(value = "/usernameError", method = RequestMethod.GET)
    public String usernameError() {
        return "/usernameError";
    }

    /**
     * Method used to redirect to duplicate email error page
     *
     * @return
     */
    @RequestMapping(value = "/emailError", method = RequestMethod.GET)
    public String emailError() {
        return "/emailError";
    }

    /**
     * Method used to log out the user
     *
     * @param request
     * @param response
     * @return
     */
    @RequestMapping(value = "/logout", method = RequestMethod.GET)
    public String logout(HttpServletRequest request, HttpServletResponse response) {
        final Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null) {
            new SecurityContextLogoutHandler().logout(request, response, auth);
        }
        return "redirect:/";
    }
}
