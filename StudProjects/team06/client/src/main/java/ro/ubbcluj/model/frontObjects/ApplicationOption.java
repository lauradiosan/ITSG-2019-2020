package ro.ubbcluj.model.frontObjects;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * This class is used for finding available rooms for a application
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ApplicationOption {

    private String announcementId;
    private String startDate;
    private String endDate;

}
