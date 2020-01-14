package ro.ubbcluj.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import ro.ubbcluj.model.frontObjects.LoginPurposes;

/**
 * @author dianat2
 */
@Slf4j
@Controller
public class ImageController {

    @RequestMapping(value = "/", method = RequestMethod.POST)
    public String getClassForImageFromServer(@ModelAttribute(value = "loginPurposes") LoginPurposes loginPurposes, Model model,
                                             RedirectAttributes redirectAttributes) {
        System.out.println("suntem in encode");
        final String data = loginPurposes.getData();
        System.out.println(data);
        final String uri = "http://0.0.0.0:5000/login";

        RestTemplate restTemplate = new RestTemplate();

        final String replacedString = data.replace("data:image/png;base64,", "");
        String result = restTemplate.postForObject(uri, replacedString, String.class);

        System.out.println(result);
        loginPurposes.setData(result);
        redirectAttributes.addFlashAttribute("loginPurposes", loginPurposes);
        redirectAttributes.addFlashAttribute("username", result);
        redirectAttributes.addFlashAttribute("password", result);
        System.out.println(redirectAttributes.containsAttribute("username"));
        return "redirect:/";
//        return "index";
    }

}
