package ro.ubbcluj.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ro.ubbcluj.entity.Account;

public interface AccountRepository extends JpaRepository<Account, Long> {

    Account findByUsername(String username);

}