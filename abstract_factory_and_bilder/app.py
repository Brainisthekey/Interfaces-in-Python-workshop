from abc import ABC, abstractmethod
from enum import Enum
from typing import Union
from pydantic import BaseModel


class SystemType(Enum):
    WIN = 'win'
    MACOS = 'macos'
    LINUX = 'linux'


class WinPackages(Enum):
    APP = 'exe'

class LinuxPackages(Enum):
    APP = 'deb'

class MacOSPackage(Enum):
    APP = 'app'


class DeploymentStatus(Enum):
    SUCCESS = 'success'
    ERROR = 'error'


class MetaPackage(BaseModel):
    path_to_file: str
    os_system: SystemType
    package_type: Union[WinPackages, LinuxPackages, MacOSPackage]


class AbstractPackagesFactory(ABC):

    @abstractmethod
    def deploy(self, path_to_file: str) -> DeploymentStatus:
        pass


class AbstractPayloadFactory(ABC):
    
    @abstractmethod
    def prepare_package(
        self,
        package_type: Union[WinPackages, LinuxPackages, MacOSPackage]
    ) -> AbstractPackagesFactory:
        raise NotImplementedError()


class MacOSFactory(AbstractPayloadFactory):

    def prepare_package(self, package_type: MacOSPackage) -> AbstractPackagesFactory:
        match package_type:
            case MacOSPackage.APP:
                print('The payload factory for current type of app is MacOSAppFactory')
                return MacOSAppFactory()

class WindowsFactory(AbstractPayloadFactory):

    def prepare_package(self, package_type: WinPackages) -> AbstractPackagesFactory:
        match package_type:
            case WinPackages.APP:
                return WindowsExeFactory()

class LinuxFactory(AbstractPayloadFactory):

    def prepare_package(self, package_type: LinuxPackages) -> AbstractPackagesFactory:
        match package_type:
            case LinuxPackages.APP:
                return LinuxDepFactory()


class MacOSAppFactory(AbstractPackagesFactory):
    
    def deploy(self, path_to_file: str) -> DeploymentStatus:
        # The deployments steps
        ...
        return DeploymentStatus.SUCCESS

class WindowsExeFactory(AbstractPackagesFactory):

    def deploy(self, path_to_file: str) -> DeploymentStatus:
        ...

class LinuxDepFactory(AbstractPackagesFactory):

    def deploy(self, path_to_file: str) -> DeploymentStatus:
        ...



class FactoryBuilder:

    @classmethod
    def get_factory(cls, os_type: SystemType) -> AbstractPayloadFactory:
        match os_type:
            case SystemType.WIN:
                return WindowsFactory()
            case SystemType.MACOS:
                print('The factory for current payload is MacOSFactory')
                return MacOSFactory()
            case SystemType.LINUX:
                return LinuxFactory()


def main(package: MetaPackage) -> DeploymentStatus:
    result = FactoryBuilder.get_factory(
        os_type=package.os_system
    ).prepare_package(
        package_type=package.package_type
    ).deploy(
        path_to_file=package.path_to_file
    )
    return result


package = MetaPackage(path_to_file='dummy', os_system=SystemType.MACOS, package_type=MacOSPackage.APP)
print(main(package))
