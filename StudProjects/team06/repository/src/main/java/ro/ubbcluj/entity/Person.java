package ro.ubbcluj.entity;

import lombok.*;

import javax.persistence.*;


/**
 * The Person class creates an entity with various
 * attributes, and related behaviour.
 */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Person {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(mappedBy = "person")
    private Account account;

    private String firstName;
    private String lastName;
    private String email;
    private boolean active;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "role_id")
    private Role role;

    private String skills;

    /**
     * Constructor.
     *
     * @param firstName (required) the firstName of the person.
     * @param lastName  (required) the lastName of the person.
     * @param email     (required) the email of the person.
     * @param role      (required) the role of the person.
     */
    public Person(String firstName, String lastName, String email, Role role) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.role = role;
    }

}
