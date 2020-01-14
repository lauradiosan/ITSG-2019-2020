package ro.ubbcluj.interfaces;

import ro.ubbcluj.dto.ChildDTO;
import ro.ubbcluj.dto.UserDTO;

public interface UserService {


    UserDTO findByUsername(String username);

    boolean checkUsername(String username);

    void createUser(ChildDTO childDTO);

}
