from enum import Enum
from pydantic import BaseModel


class SystemType(Enum):
    WIN = 'win'
    MACOS = 'macos'
    LINUX = 'linux'

class DeploymentStatus(Enum):
    SUCCESS = 'success'
    ERROR = 'error'

class PackageType(Enum):
    EXE = 'exe'
    APP = 'app'
    DEP = 'dep'


class MetaPackage(BaseModel):
    path_to_file: str
    os_system: SystemType
    package_type: PackageType


class PackageManager:

    def __init__(self, package: MetaPackage):
        self.package = package

    def prepare_package(self) -> None:
        match self.package.os_system:
            case SystemType.WIN:
                self._prepare_win_package()
            case SystemType.MACOS:
                self._prepare_mac_os_package()
            case SystemType.LINUX:
                self._prepare_linux_package()
            case _:
                ...
    
    def deploy_package(self) -> DeploymentStatus:
        match self.package.os_system:
            case SystemType.WIN:
                self._deploy_win_package()
            case SystemType.MACOS:
                self._deploy_macos_package()
            case SystemType.LINUX:
                self._deploy_linux_package()
            case _:
                ...

    def _prepare_mac_os_package(self):
        match self.package.package_type:
            case PackageType.APP:
                ...
            case _:
                ...
    
    def _prepare_win_package(self):
        match self.package.package_type:
            case PackageType.EXE:
                ...
            case _:
                ...
    
    def _prepare_linux_package(self):
        match self.package.package_type:
            case PackageType.DEP:
                ...
            case _:
                ...
    
    def _deploy_win_package(self):
        match self.package.package_type:
            case PackageType.EXE:
                ...
            case _:
                ...

    def _deploy_macos_package(self):
        match self.package.package_type:
            case PackageType.APP:
                ...
            case _:
                ...
    
    def _deploy_linux_package(self):
        match self.package.package_type:
            case PackageType.DEP:
                ...
            case _:
                ...


def main(package: MetaPackage) -> DeploymentStatus:
    manager = PackageManager(package)
    manager.prepare_package()
    manager.deploy_package()


package = MetaPackage(path_to_file='dummy', os_system=SystemType.MACOS, package_type=PackageType.APP)
main(package)
