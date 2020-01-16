package ro.ubbcluj.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import ro.ubbcluj.entity.Person;
import ro.ubbcluj.enums.RoleEnum;

public interface PersonRepository extends JpaRepository<Person, Long> {

    Page<Person> findAllByRole_role(RoleEnum role, Pageable pageable);

}
