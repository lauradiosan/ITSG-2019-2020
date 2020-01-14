package ro.ubbcluj.dto;

import lombok.*;
import ro.ubbcluj.enums.GenderEnum;
import ro.ubbcluj.enums.RoleEnum;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * This class is used to transfer data from the user interface to server and backwards
 */
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {

    private Long id;
    private String username;
    private String password;
    private String confirmPassword;
    private String firstName;
    private String lastName;
    private String email;
    private RoleEnum role;
    private Long announcement;
    private Date birthDate;
    private GenderEnum gender;
    private String address;
    private String skills;
    private String bio;
    private Date registrationDate;
    private boolean active;

    @Override
    public String toString() {
        SimpleDateFormat ft =
                new SimpleDateFormat("yy-MM-dd");
        return String.format(
                "User [Username='%s', First Name='%s', Last Name='%s', Email='%s', Role='%s', Date='%s', Gender='%s']",
                username, firstName, lastName, email, role, ft.format(birthDate), gender
        );
    }

}
