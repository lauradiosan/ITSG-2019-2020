package ro.ubbcluj.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import ro.ubbcluj.dto.ChildDTO;
import ro.ubbcluj.interfaces.ChildrenService;
import ro.ubbcluj.interfaces.StorageService;
import ro.ubbcluj.interfaces.UserService;
import ro.ubbcluj.pagination.PageWrapper;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

/**
 * @author dianat2
 */
@Controller
public class ChildrenController {

    @Autowired
    ChildrenService childrenService;

    @Autowired
    UserService userService;

    @Autowired
    private StorageService storageService;

    @RequestMapping(value = "/children", method = RequestMethod.GET)
    public String getAllChildren(Model model,
                                 @RequestParam("page") Optional<Integer> pageNumber,
                                 @RequestParam("size") Optional<Integer> pageSize) {
        PageRequest pageRequest = new PageRequest(pageNumber.orElse(0), pageSize.orElse(5));
        Page<ChildDTO> childDTOPage = childrenService.getAll(pageRequest);
        PageWrapper<ChildDTO> page;

        page = new PageWrapper<>(childDTOPage, "/children");
        model.addAttribute("preschoolers", childDTOPage);
        model.addAttribute("page", page);

        List<Integer> pageSizes = Arrays.asList(5, 15, 30);
        model.addAttribute("pageSizes", pageSizes);
        return "childrenList";
    }

    @RequestMapping(value = "/addChild", method = RequestMethod.GET)
    public String addChild(Model model) {
        model.addAttribute("childDTO", new ChildDTO());
        return "uploadFile";
    }

    @RequestMapping(value = "/addChild", method = RequestMethod.POST)
    public String addChild(Model model, ChildDTO childDTO) {
        if (userService.checkUsername(childDTO.getLastName() + childDTO.getFirstName())) {
            return "/usernameError";
        } else {
            storageService.store(childDTO.getFile(), childDTO.getLastName() + childDTO.getFirstName());
            userService.createUser(childDTO);
            model.addAttribute("childDTO", childDTO);
            return "redirect:/children";
        }
    }

}
