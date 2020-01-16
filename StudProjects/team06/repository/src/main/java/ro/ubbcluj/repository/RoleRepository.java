package ro.ubbcluj.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ro.ubbcluj.entity.Role;
import ro.ubbcluj.enums.RoleEnum;

public interface RoleRepository extends JpaRepository<Role, Long> {

    Role findByRole(RoleEnum roleEnum);

}
