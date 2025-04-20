"""
Data models for the configuration system.
These models define the structure of the launcher configuration.
"""
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from src.models.constants import APP_NAME, APP_VERSION

@dataclass
class ModConfig:
    """
    Represents a single mod configuration.
    """
    name: str
    target_path: str
    download_url: str
    description: str = ""
    version: str = "1.0.0"
    is_required: bool = False
    id: Optional[str] = None  # Unique identifier for the mod

    def __post_init__(self):
        """
        Ensure the ID is set if not provided
        """
        if self.id is None:
            # Create an ID from the name if none provided
            self.id = str(uuid.uuid4())

    def to_dict(self) -> Dict:
        """
        Convert to dictionary for serialization
        """
        return {
            "id": self.id,
            "name": self.name,
            "target_path": self.target_path,
            "download_url": self.download_url,
            "description": self.description,
            "version": self.version,
            "is_required": self.is_required
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ModConfig':
        """
        Create from dictionary
        """
        return cls(
            id=data.get("id"),
            name=data["name"],
            target_path=data["target_path"],
            download_url=data["download_url"],
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            is_required=data.get("is_required", False)
        )


@dataclass
class LauncherConfig:
    """
    Main configuration for the launcher.
    """
    name: str
    game_exe: str
    description: str = ""
    version: str = "1.0.0"
    mods: List[ModConfig] = field(default_factory=list)
    validation_files: List[str] = field(default_factory=list)
    default_locations: List[str] = field(default_factory=list)
    target_os: str = "windows"  # windows, macos, linux
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """
        Convert to dictionary for serialization
        """
        return {
            "name": self.name,
            "game_exe": self.game_exe,
            "description": self.description,
            "version": self.version,
            "mods": [mod.to_dict() for mod in self.mods],
            "validation_files": self.validation_files,
            "default_locations": self.default_locations,
            "target_os": self.target_os,
            "created_with": f"{APP_NAME} v{APP_VERSION}",
            "created": self.created,
            "updated": datetime.now().isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'LauncherConfig':
        """
        Create from dictionary
        """
        return cls(
            name=data["name"],
            game_exe=data["game_exe"],
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            mods=[ModConfig.from_dict(mod) for mod in data.get("mods", [])],
            validation_files=data.get("validation_files", []),
            default_locations=data.get("default_locations", []),
            target_os=data.get("target_os", "windows"),
            created=data.get("created", datetime.now().isoformat()),
            updated=data.get("updated", datetime.now().isoformat())
        )

    def add_mod(self, mod: ModConfig) -> None:
        """
        Add a mod to the configuration
        """
        self.mods.append(mod)
        self.updated = datetime.now().isoformat()

    def remove_mod(self, mod_id: str) -> bool:
        """
        Remove a mod from the configuration
        Returns True if mod was found and removed
        """
        initial_count = len(self.mods)
        self.mods = [mod for mod in self.mods if mod.id != mod_id]
        was_removed = len(self.mods) < initial_count

        if was_removed:
            self.updated = datetime.now().isoformat()

        return was_removed

    def add_validation_file(self, file_path: str) -> None:
        """
        Add a validation file
        """
        if file_path not in self.validation_files:
            self.validation_files.append(file_path)
            self.updated = datetime.now().isoformat()

    def remove_validation_file(self, file_path: str) -> bool:
        """
        Remove a validation file
        Returns True if file was found and removed
        """
        if file_path in self.validation_files:
            self.validation_files.remove(file_path)
            self.updated = datetime.now().isoformat()
            return True
        return False

    def add_default_location(self, location: str) -> None:
        """
        Add a default game location
        """
        if location not in self.default_locations:
            self.default_locations.append(location)
            self.updated = datetime.now().isoformat()

    def remove_default_location(self, location: str) -> bool:
        """
        Remove a default game location
        Returns True if location was found and removed
        """
        if location in self.default_locations:
            self.default_locations.remove(location)
            self.updated = datetime.now().isoformat()
            return True
        return False
