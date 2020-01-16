package ro.ubbcluj.interfaces;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import ro.ubbcluj.dto.ChildDTO;

/**
 * @author dianat2
 */
public interface ChildrenService {

    Page<ChildDTO> getAll(Pageable pageable);

}
