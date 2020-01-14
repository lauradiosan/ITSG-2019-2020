package ro.ubbcluj.pagination;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.domain.Page;

import java.util.ArrayList;
import java.util.List;

/**
 * This class is used for pagination
 *
 * @param <T>
 */
@Getter
@Setter
@NoArgsConstructor
public class PageWrapper<T> {

    public static final int MAX_PAGE = 5;
    public static final int HALF_MAX_PAGE = MAX_PAGE / 2;
    private static final int DIFF_PAGES = MAX_PAGE - HALF_MAX_PAGE;

    private Page<T> page;
    private List<PageItem> pageItems;
    private int currentPage;
    private String url;

    public PageWrapper(Page<T> page, String url) {
        this.page = page;
        this.url = url;
        this.pageItems = new ArrayList<>();
        getItems(page);
    }

    private void getItems(Page<T> page) {

        currentPage = page.getNumber() + 1;

        int start, size;
        int totalPages = page.getTotalPages();

        if (totalPages <= MAX_PAGE) {
            start = 1;
            size = totalPages;
        } else {
            size = MAX_PAGE;
            if (currentPage <= DIFF_PAGES) {
                start = 1;
            } else if (currentPage >= totalPages - HALF_MAX_PAGE) {
                start = totalPages - MAX_PAGE + 1;
            } else {
                start = currentPage - HALF_MAX_PAGE;
            }
        }

        for (int i = 0; i < size; i++) {
            addToPage(new PageItem((start + i), (start + i) == currentPage));
        }
    }

    private void addToPage(PageItem pageItem) {
        this.pageItems.add(pageItem);
    }

    public List<PageItem> getItems() {
        return pageItems;
    }

    public int getNumber() {
        return currentPage;
    }

    public List<T> getContent() {
        return page.getContent();
    }

    public int getSize() {
        return page.getSize();
    }

    public int getTotalPages() {
        return page.getTotalPages();
    }

    public boolean isFirstPage() {
        return page.isFirst();
    }

    public boolean isLastPage() {
        return page.isLast();
    }

    public boolean isHasPreviousPage() {
        return page.hasPrevious();
    }

    public boolean isHasNextPage() {
        return page.hasNext();
    }

}
