package ro.ubbcluj.entity;

import lombok.*;

import javax.persistence.*;
import java.util.Date;


/**
 * The Account class creates an entity with various
 * attributes, and related behaviour.
 * The Account is needed by every client
 * in order to use the HMS application
 */
@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String password;
    private Date registrationDate;
    private boolean active;

    @OneToOne
    @JoinColumn(name = "person_id")
    private Person person;

    /**
     * Constructor.
     *
     * @param username         (required) the user title of the account.
     * @param password         (required) the password of the account.
     * @param registrationDate (required) the registration date of the account.
     */
    public Account(String username, String password, Person person, Date registrationDate) {
        this.username = username;
        this.password = password;
        this.person = person;
        this.registrationDate = registrationDate;
    }

}
