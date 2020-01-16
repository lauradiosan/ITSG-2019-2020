package ro.ubbcluj.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.util.FileSystemUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;
import ro.ubbcluj.config.StorageProperties;
import ro.ubbcluj.exception.StorageException;
import ro.ubbcluj.exception.StorageFileNotFoundException;
import ro.ubbcluj.interfaces.StorageService;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.stream.Stream;

@Service
public class FileSystemStorageService implements StorageService {

    private final Path rootLocation;

    private final String storageRootLocation;
    private String directoryName;

    @Autowired
    public FileSystemStorageService(StorageProperties properties) {
        this.rootLocation = Paths.get(properties.getLocation());
        this.storageRootLocation = properties.getLocation();
    }

    @Override
    public void store(MultipartFile file, String directoryName) {
        String filename = StringUtils.cleanPath(file.getOriginalFilename());
        try {
            if (file.isEmpty()) {
                throw new StorageException("Failed to store empty file " + filename);
            }
            if (filename.contains("..")) {
                // This is a security check
                throw new StorageException(
                        "Cannot store file with relative path outside current directory "
                                + filename);
            }
            try (InputStream inputStream = file.getInputStream()) {
                this.directoryName = directoryName;
                final Path customPath = Paths.get(this.storageRootLocation + directoryName + File.separator);
                Files.createDirectories(customPath);
                Files.copy(inputStream, customPath.resolve(filename), StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException e) {
            throw new StorageException("Failed to store file " + filename, e);
        }
    }

    @Override
    public Stream<Path> loadAll() {
        try {
            final Path rootLocation = this.rootLocation;
            return Files.walk(rootLocation, 1)
                    .filter(path -> !path.equals(rootLocation))
                    .map(rootLocation::relativize);
        } catch (IOException e) {
            throw new StorageException("Failed to read stored files", e);
        }

    }

    @Override
    public Path load(String filename) {
        return this.rootLocation.resolve(this.directoryName + filename);
    }

    @Override
    public Resource loadAsResource(String filename) {
        try {
            Path file = load(filename);
            Resource resource = new UrlResource(file.toUri());
            if (resource.exists() || resource.isReadable()) {
                return resource;
            } else {
                throw new StorageFileNotFoundException(
                        "Could not read file: " + filename);
            }
        } catch (MalformedURLException e) {
            throw new StorageFileNotFoundException("Could not read file: " + filename, e);
        }
    }

    @Override
    public void deleteAll() {
        FileSystemUtils.deleteRecursively(this.rootLocation.toFile());
    }

    @Override
    public void init() {
        try {
            Files.createDirectories(this.rootLocation);
        } catch (IOException e) {
            throw new StorageException("Could not initialize storage", e);
        }
    }

    private Path getRootLocation() {
        return Paths.get(this.storageRootLocation + directoryName);
    }

}
