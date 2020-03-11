from django.core.management.base import BaseCommand, CommandError

from inventory.models import Asset


class Command(BaseCommand):

    help = "Audit the contents of an asset."

    def handle(self, *args, **options):
        asset_code = input("Scan asset code: ")
        asset = Asset.objects.filter(asset_code=asset_code).get()
        if not asset.asset_model.is_container:
            raise CommandError("Must be a container.")
        self.audit_container(asset)

    def audit_container(self, asset: Asset) -> None:
        print(f"Auditing: {asset}")

        expected_assets = set()
        found_assets = set()
        for sub_asset in asset.asset_set.all():
            expected_assets.add(sub_asset)

        while True:
            try:
                code = str(input("Scan contents or container to finish: "))
                sub_asset = Asset.objects.filter(asset_code=code).get()
                if sub_asset == asset:
                    print(self.style.SUCCESS("Finished scanning, processing."))
                    break
                if sub_asset in found_assets:
                    print(f"Already seen {sub_asset}")
                    continue
                if sub_asset not in expected_assets:
                    print(self.style.WARNING(f"Did not expect {sub_asset}"))
                found_assets.add(sub_asset)
            except Asset.DoesNotExist:
                print(self.style.ERROR(f"No such asset {code}"))

        lost_assets = expected_assets - found_assets
        new_assets = found_assets - expected_assets

        for lost in lost_assets:
            print(self.style.ERROR(f"Did not see {lost}, moving to Unknown"))
            lost.location = Asset.objects.filter(asset_code="SRO-UNK-WNW").get()
            lost.save()

        for new in new_assets:
            print(self.style.WARNING(f"Found {new}, expected to find in {new.location}, moving to {asset}"))
            new.location = asset
            new.save()
