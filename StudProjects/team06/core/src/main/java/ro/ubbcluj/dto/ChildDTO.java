package ro.ubbcluj.dto;

import lombok.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * @author dianat2
 */
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ChildDTO {

    private String firstName;
    private String lastName;
    private MultipartFile file;

}
