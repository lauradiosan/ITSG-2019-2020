package ro.ubbcluj.pagination;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * This class is used for pagination
 */
@AllArgsConstructor
@Getter
@Setter
@NoArgsConstructor
public class PageItem {

    private int number;
    private boolean current;

}
