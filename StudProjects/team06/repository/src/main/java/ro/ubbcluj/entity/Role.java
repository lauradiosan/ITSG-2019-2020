package ro.ubbcluj.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import ro.ubbcluj.enums.RoleEnum;

import javax.persistence.*;
import java.util.List;

/**
 * The Role class creates an entity with various
 * attributes, and related behaviour.
 */
@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Role {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Enumerated(EnumType.STRING)
    private RoleEnum role;

    @OneToMany(mappedBy = "role")
    private List<Person> person;

    /**
     * Constructor.
     *
     * @param role (required) the type of the role.
     */
    public Role(RoleEnum role) {
        this.role = role;
    }


    @Override
    public String toString() {
        return String.format(
                "Role [Role='%s']",
                role
        );
    }

}
